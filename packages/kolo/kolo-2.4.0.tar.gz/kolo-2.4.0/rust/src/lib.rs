#[cfg(not(PyPy))]
#[path = ""]
mod _kolo {
    use pyo3::exceptions::PyAttributeError;
    use pyo3::exceptions::PyKeyError;
    use pyo3::exceptions::PyTypeError;
    use pyo3::ffi;
    use pyo3::prelude::*;
    use pyo3::types::PyDict;
    use pyo3::types::PyFrame;
    use pyo3::types::PyList;
    use pyo3::types::PyTuple;
    use pyo3::types::PyType;
    use pyo3::AsPyPointer;
    use serde_json::json;
    use std::collections::HashMap;
    use std::env::current_dir;
    use std::path::Path;
    use std::time::SystemTime;
    use ulid::Ulid;

    fn timestamp() -> f64 {
        SystemTime::now()
            .duration_since(SystemTime::UNIX_EPOCH)
            .expect("System time is before unix epoch")
            .as_secs_f64()
    }

    fn frame_path(frame: &PyFrame) -> Result<String, PyErr> {
        let f_code = frame.getattr("f_code")?;
        let co_filename = f_code.getattr("co_filename")?;
        let filename = co_filename.extract::<String>()?;
        let path = Path::new(&filename).canonicalize().unwrap();
        let dir = current_dir()
            .expect("Current directory is invalid")
            .canonicalize()
            .unwrap();
        let relative_path = match path.strip_prefix(&dir) {
            Ok(relative_path) => relative_path,
            Err(_) => &path,
        };
        let lineno = frame.getattr("f_lineno")?;
        Ok(format!("{}:{}", relative_path.display(), lineno))
    }

    fn get_qualname(frame: &PyFrame, py: Python) -> Result<Option<String>, PyErr> {
        let f_code = frame.getattr("f_code")?;
        match f_code.getattr("co_qualname") {
            Ok(qualname) => {
                let globals = frame.getattr("f_globals")?;
                let module = globals.get_item("__name__")?;
                return Ok(Some(format!("{}.{}", module, qualname)));
            }
            Err(err) if err.is_instance_of::<PyAttributeError>(py) => {}
            Err(err) => return Err(err),
        }

        let co_name = f_code.getattr("co_name")?;
        let name = co_name.extract::<String>()?;
        if name.as_str() == "<module>" {
            let globals = frame.getattr("f_globals")?;
            let module = globals.get_item("__name__")?;
            return Ok(Some(format!("{}.<module>", module)));
        }

        match get_qualname_fallback(frame, py, co_name) {
            Ok(qualname) => Ok(qualname),
            Err(_) => Ok(None),
        }
    }

    fn get_qualname_fallback(
        frame: &PyFrame,
        py: Python,
        co_name: &PyAny,
    ) -> Result<Option<String>, PyErr> {
        let outer_frame = frame.getattr("f_back")?;
        if outer_frame.is_none() {
            return Ok(None);
        }

        let outer_frame_locals = outer_frame.getattr("f_locals")?;
        match outer_frame_locals.get_item(co_name) {
            Ok(function) => {
                let module = function.getattr("__module__")?;
                let qualname = function.getattr("__qualname__")?;
                return Ok(Some(format!("{}.{}", module, qualname)));
            }
            Err(err) if err.is_instance_of::<PyKeyError>(py) => {}
            Err(_) => return Ok(None),
        }

        let locals = frame.getattr("f_locals")?;
        let inspect = PyModule::import(py, "inspect")?;
        let getattr_static = inspect.getattr("getattr_static")?;
        match locals.get_item("self") {
            Ok(locals_self) => {
                let function = getattr_static.call1((locals_self, co_name))?;
                let builtins = py.import("builtins")?;
                let property = builtins.getattr("property")?;
                let property = property.extract()?;
                let function = match function.is_instance(property)? {
                    true => function.getattr("fget")?,
                    false => function,
                };
                let module = function.getattr("__module__")?;
                let qualname = function.getattr("__qualname__")?;
                return Ok(Some(format!("{}.{}", module, qualname)));
            }
            Err(err) if err.is_instance_of::<PyKeyError>(py) => {}
            Err(_) => return Ok(None),
        };

        match locals.get_item("cls") {
            Ok(cls) if cls.is_instance_of::<PyType>()? => {
                let function = getattr_static.call1((cls, co_name))?;
                let module = function.getattr("__module__")?;
                let qualname = function.getattr("__qualname__")?;
                return Ok(Some(format!("{}.{}", module, qualname)));
            }
            Ok(_) => {}
            Err(err) if err.is_instance_of::<PyKeyError>(py) => {}
            Err(_) => return Ok(None),
        }
        let globals = frame.getattr("f_globals")?;
        match locals.get_item("__qualname__") {
            Ok(qualname) => {
                let module = globals.get_item("__name__")?;
                Ok(Some(format!("{}.{}", module, qualname)))
            }
            Err(err) if err.is_instance_of::<PyKeyError>(py) => {
                let function = globals.get_item(co_name)?;
                let module = function.getattr("__module__")?;
                let qualname = function.getattr("__qualname__")?;
                Ok(Some(format!("{}.{}", module, qualname)))
            }
            Err(_) => Ok(None),
        }
    }

    fn dump_json(py: Python, data: &PyAny) -> Result<serde_json::Value, PyErr> {
        let json = PyModule::import(py, "json")?;
        let serialize = PyModule::import(py, "kolo.serialize")?;
        let kolo_json_encoder = serialize.getattr("KoloJSONEncoder")?;
        let args = PyTuple::new(py, [&data]);
        let kwargs = PyDict::new(py);
        kwargs.set_item("cls", kolo_json_encoder)?;
        kwargs.set_item("skipkeys", true)?;
        let json_data = json.call_method("dumps", args, Some(kwargs))?;
        let json_data = json_data.extract::<String>()?;
        let json_data: serde_json::Value = serde_json::from_str(&json_data)
            .expect("Serde json could not load json value dumped by python.");
        Ok(json_data)
    }

    fn use_django_filter(filename: &str) -> bool {
        #[cfg(target_os = "windows")]
        let middleware_path = "\\kolo\\middleware.py";
        #[cfg(not(target_os = "windows"))]
        let middleware_path = "/kolo/middleware.py";

        filename.contains(middleware_path)
    }

    fn use_django_template_filter(filename: &str) -> bool {
        #[cfg(target_os = "windows")]
        let template_path = "django\\template\\backends\\django.py";
        #[cfg(not(target_os = "windows"))]
        let template_path = "django/template/backends/django.py";

        filename.contains(template_path)
    }

    fn use_celery_filter(filename: &str) -> bool {
        filename.contains("celery") && !(filename.contains("sentry_sdk"))
    }

    fn use_huey_filter(
        filename: &str,
        huey_filter: &PyAny,
        py: Python,
        pyframe: &PyFrame,
    ) -> Result<bool, PyErr> {
        #[cfg(target_os = "windows")]
        let huey_path = "\\huey\\api.py";
        #[cfg(not(target_os = "windows"))]
        let huey_path = "/huey/api.py";

        if filename.contains(huey_path) {
            let task_class = huey_filter.getattr("klass")?;
            if task_class.is_none() {
                let huey_api = PyModule::import(py, "huey.api")?;
                let task_class = huey_api.getattr("Task")?;
                huey_filter.setattr("klass", task_class)?;
            }

            let task_class = huey_filter.getattr("klass")?;
            let task_class = task_class.downcast()?;
            let frame_locals = pyframe.getattr("f_locals")?;
            let task = frame_locals.get_item("self")?;
            task.is_instance(task_class)
        } else {
            Ok(false)
        }
    }

    fn use_requests_filter(filename: &str) -> bool {
        #[cfg(target_os = "windows")]
        let requests_path = "requests\\sessions";
        #[cfg(not(target_os = "windows"))]
        let requests_path = "requests/sessions";

        filename.contains(requests_path)
    }

    fn use_urllib_filter(filename: &str) -> bool {
        #[cfg(target_os = "windows")]
        let urllib_path = "urllib\\request";
        #[cfg(not(target_os = "windows"))]
        let urllib_path = "urllib/request";

        filename.contains(urllib_path)
    }

    fn use_urllib3_filter(filename: &str) -> bool {
        #[cfg(target_os = "windows")]
        let urllib3_path = "urllib3\\connectionpool";
        #[cfg(not(target_os = "windows"))]
        let urllib3_path = "urllib3/connectionpool";

        filename.contains(urllib3_path)
    }

    fn use_exception_filter(filename: &str, event: &str) -> bool {
        event == "call" && filename.contains("django")
    }

    fn use_logging_filter(filename: &str, event: &str) -> bool {
        #[cfg(target_os = "windows")]
        let logging_path = "\\logging\\";
        #[cfg(not(target_os = "windows"))]
        let logging_path = "/logging/";

        event == "return" && filename.contains(logging_path)
    }

    fn use_sql_filter(
        filename: &str,
        sql_filter: &PyAny,
        py: Python,
        pyframe: &PyFrame,
    ) -> Result<bool, PyErr> {
        #[cfg(target_os = "windows")]
        let sql_path = "\\django\\db\\models\\sql\\compiler.py";
        #[cfg(not(target_os = "windows"))]
        let sql_path = "/django/db/models/sql/compiler.py";

        if filename.contains(sql_path) {
            let sql_filter_class = sql_filter.get_type();
            if sql_filter_class.getattr("klass")?.is_none() {
                let compiler = PyModule::import(py, "django.db.models.sql.compiler")?;
                let sql_update_compiler = compiler.getattr("SQLUpdateCompiler")?;
                sql_filter_class.setattr("klass", sql_update_compiler)?;
            }
            let f_code = pyframe.getattr("f_code")?;
            Ok(!f_code.is(sql_filter_class
                .getattr("klass")?
                .getattr("execute_sql")?
                .getattr("__code__")?))
        } else {
            Ok(false)
        }
    }

    fn use_pytest_filter(filename: &str, event: &str) -> bool {
        #[cfg(target_os = "windows")]
        let pytest_path = "kolo\\pytest_plugin.py";
        #[cfg(not(target_os = "windows"))]
        let pytest_path = "kolo/pytest_plugin.py";

        event == "call" && filename.contains(pytest_path)
    }

    fn use_unittest_filter(filename: &str, event: &str) -> bool {
        #[cfg(target_os = "windows")]
        let unittest_path = "unittest\\result.py";
        #[cfg(not(target_os = "windows"))]
        let unittest_path = "unittest/result.py";

        event == "call" && filename.contains(unittest_path)
    }

    fn process_default_include_frames(
        py: Python,
        obj: &mut KoloProfiler,
        frame: &PyObject,
        pyframe: &PyFrame,
        event: &str,
        arg: &PyObject,
        name: &str,
        filename: &str,
    ) -> Result<bool, PyErr> {
        let filter = match name {
            "get_response" => {
                if use_django_filter(filename) {
                    obj.default_include_frames[0].as_ref(py)
                } else {
                    return Ok(false);
                }
            }
            "render" => {
                if use_django_template_filter(filename) {
                    obj.default_include_frames[1].as_ref(py)
                } else {
                    return Ok(false);
                }
            }
            "apply_async" => {
                if use_celery_filter(filename) {
                    obj.default_include_frames[2].as_ref(py)
                } else {
                    return Ok(false);
                }
            }
            "execute" => {
                let huey_filter = obj.default_include_frames[3].as_ref(py);
                if use_huey_filter(filename, huey_filter, py, pyframe)? {
                    huey_filter
                } else {
                    return Ok(false);
                }
            }
            "send" => {
                if use_requests_filter(filename) {
                    obj.default_include_frames[4].as_ref(py)
                } else {
                    return Ok(false);
                }
            }
            "do_open" => {
                if use_urllib_filter(filename) {
                    obj.default_include_frames[5].as_ref(py)
                } else {
                    return Ok(false);
                }
            }
            "urlopen" => {
                if use_urllib3_filter(filename) {
                    obj.default_include_frames[6].as_ref(py)
                } else {
                    return Ok(false);
                }
            }
            "handle_uncaught_exception" => {
                if use_exception_filter(filename, event) {
                    obj.default_include_frames[7].as_ref(py)
                } else {
                    return Ok(false);
                }
            }
            "_log" => {
                if use_logging_filter(filename, event) {
                    obj.default_include_frames[8].as_ref(py)
                } else {
                    return Ok(false);
                }
            }
            "execute_sql" => {
                let sql_filter = obj.default_include_frames[9].as_ref(py);
                if use_sql_filter(filename, sql_filter, py, pyframe)? {
                    sql_filter
                } else {
                    return Ok(false);
                }
            }
            "startTest" => {
                if use_unittest_filter(filename, event) {
                    obj.default_include_frames[10].as_ref(py)
                } else {
                    return Ok(false);
                }
            }
            "stopTest" => {
                if use_unittest_filter(filename, event) {
                    obj.default_include_frames[10].as_ref(py)
                } else {
                    return Ok(false);
                }
            }
            "pytest_runtest_logstart" => {
                if use_pytest_filter(filename, event) {
                    obj.default_include_frames[11].as_ref(py)
                } else {
                    return Ok(false);
                }
            }
            "pytest_runtest_logfinish" => {
                if use_pytest_filter(filename, event) {
                    obj.default_include_frames[11].as_ref(py)
                } else {
                    return Ok(false);
                }
            }
            _ => return Ok(false),
        };

        let py_event = event.to_object(py);
        let call_frames = PyList::new(py, &obj.call_frames);
        let args = PyTuple::new(py, [frame, &py_event, arg, &call_frames.into()]);
        let data = filter.call_method1("process", args)?;

        let json_data = dump_json(py, data)?;
        obj.frames_of_interest.push(json_data);
        if obj.one_trace_per_test {
            let frame_type = data.get_item("type")?;
            let frame_type = frame_type.extract()?;
            match frame_type {
                "start_test" => {
                    let trace_id = Ulid::new();
                    let trace_id = format!("trc_{}", trace_id.to_string());
                    obj.trace_id = trace_id;

                    obj.start_test_index = obj.frames_of_interest.len() - 1;
                }
                "end_test" => {
                    obj.save_in_db(py, Some(&obj.frames_of_interest[obj.start_test_index..]))?;
                }
                _ => {}
            }
        }
        Ok(true)
    }

    fn library_filter(co_filename: &str) -> bool {
        #[cfg(target_os = "windows")]
        let paths = ["lib\\python", "\\site-packages\\", "\\x64\\lib\\"];
        #[cfg(not(target_os = "windows"))]
        let paths = ["lib/python", "/site-packages/"];

        for path in paths {
            if co_filename.contains(path) {
                return true;
            }
        }
        if cfg!(not(windows)) {
            false
        } else {
            (co_filename.contains("\\python\\") || co_filename.contains("\\Python\\"))
                && (co_filename.contains("\\lib\\") || co_filename.contains("\\Lib\\"))
        }
    }

    fn frozen_filter(co_filename: &str) -> bool {
        co_filename.contains("<frozen ")
    }

    fn exec_filter(co_filename: &str) -> bool {
        co_filename.contains("<string>")
    }

    fn kolo_filter(co_filename: &str) -> bool {
        #[cfg(target_os = "windows")]
        let paths = [
            "\\kolo\\middleware",
            "\\kolo\\profiler",
            "\\kolo\\serialize",
        ];
        #[cfg(not(target_os = "windows"))]
        let paths = ["/kolo/middleware", "/kolo/profiler", "/kolo/serialize"];

        paths.iter().any(|p| co_filename.contains(p))
    }

    fn module_init_filter(co_name: &str) -> bool {
        co_name == "<module>"
    }

    fn attrs_filter(co_filename: &str, pyframe: &PyFrame) -> Result<bool, PyErr> {
        if co_filename.starts_with("<attrs generated") {
            return Ok(true);
        }

        let previous = pyframe.getattr("f_back")?;
        if previous.is_none() {
            return Ok(false);
        }

        let f_code = previous.getattr("f_code")?;
        let co_filename = f_code.getattr("co_filename")?;
        let co_filename = co_filename.extract::<String>()?;

        #[cfg(target_os = "windows")]
        let make_path = "attr\\_make.py";
        #[cfg(not(target_os = "windows"))]
        let make_path = "attr/_make.py";

        if co_filename.is_empty() {
            let previous = previous.getattr("f_back")?;
            if previous.is_none() {
                return Ok(false);
            }
            let f_code = previous.getattr("f_code")?;
            let co_filename = f_code.getattr("co_filename")?;
            let co_filename = co_filename.extract::<String>()?;
            Ok(co_filename.ends_with(make_path))
        } else {
            Ok(co_filename.ends_with(make_path))
        }
    }

    fn process_default_ignore_frames(
        pyframe: &PyFrame,
        co_name: &str,
        co_filename: &str,
    ) -> Result<bool, PyErr> {
        if library_filter(co_filename) {
            return Ok(true);
        }

        if frozen_filter(co_filename) {
            return Ok(true);
        }

        if kolo_filter(co_filename) {
            return Ok(true);
        }

        if module_init_filter(co_name) {
            return Ok(true);
        }

        if exec_filter(co_filename) {
            return Ok(true);
        }

        // We don't need a match block here because the
        // return value is already in the right format
        attrs_filter(co_filename, pyframe)
    }

    extern "C" fn profile(
        _obj: *mut ffi::PyObject,
        _frame: *mut ffi::PyFrameObject,
        what: i32,
        _arg: *mut ffi::PyObject,
    ) -> i32 {
        let event = {
            if what == ffi::PyTrace_CALL {
                "call"
            } else if what == ffi::PyTrace_RETURN {
                "return"
            } else {
                return 0;
            }
        };
        let _frame = _frame as *mut ffi::PyObject;
        Python::with_gil(|py| unsafe {
            let obj = match PyObject::from_borrowed_ptr_or_err(py, _obj) {
                Ok(obj) => obj,
                Err(err) => {
                    err.restore(py);
                    return -1;
                }
            };
            let mut profiler = match obj.extract::<PyRefMut<KoloProfiler>>(py) {
                Ok(profiler) => profiler,
                Err(err) => {
                    err.restore(py);
                    return -1;
                }
            };

            let frame = match PyObject::from_borrowed_ptr_or_err(py, _frame) {
                Ok(frame) => frame,
                Err(err) => {
                    err.restore(py);
                    return -1;
                }
            };
            let arg = match PyObject::from_borrowed_ptr_or_opt(py, _arg) {
                Some(arg) => arg,
                None => py.None(),
            };

            match profiler.profile(frame, arg, event, py) {
                Ok(_) => 0,
                Err(err) => {
                    err.restore(py);
                    -1
                }
            }
        })
    }

    #[pyclass(module = "kolo._kolo")]
    struct KoloProfiler {
        db_path: String,
        one_trace_per_test: bool,
        trace_id: String,
        frames_of_interest: Vec<serde_json::Value>,
        config: PyObject,
        include_frames: Vec<String>,
        ignore_frames: Vec<String>,
        default_include_frames: Vec<PyObject>,
        call_frames: Vec<(PyObject, String)>,
        timestamp: f64,
        _frame_ids: HashMap<usize, String>,
        start_test_index: usize,
    }

    #[pymethods]
    impl KoloProfiler {
        fn save_request_in_db(&self) -> Result<(), PyErr> {
            Python::with_gil(|py| self.save_in_db(py, None))
        }
    }

    impl KoloProfiler {
        fn save_in_db(
            &self,
            py: Python,
            frames: Option<&[serde_json::Value]>,
        ) -> Result<(), PyErr> {
            let version = PyModule::import(py, "kolo.version")?
                .getattr("__version__")?
                .extract::<String>()?;
            let commit_sha = PyModule::import(py, "kolo.git")?
                .getattr("COMMIT_SHA")?
                .extract::<String>()?;
            let argv = PyModule::import(py, "sys")?
                .getattr("argv")?
                .extract::<Vec<String>>()?;
            let frames = match frames {
                Some(frames) => frames,
                None => &self.frames_of_interest,
            };
            let data = json!({
                "command_line_args": argv,
                "current_commit_sha": commit_sha,
                "frames_of_interest": frames,
                "meta": {"version": version, "use_frame_boundaries": true},
                "timestamp": self.timestamp,
                "trace_id": self.trace_id,
            });
            let config = self.config.as_ref(py);
            let wal_mode = match config.get_item("wal_mode") {
                Ok(wal_mode) => Some(wal_mode),
                Err(_) => None,
            };
            let db = PyModule::import(py, "kolo.db")?;
            let save = db.getattr("save_invocation_in_sqlite")?;
            save.call1((&self.db_path, &self.trace_id, data.to_string(), wal_mode))?;
            Ok(())
        }

        fn process_frame(
            &mut self,
            frame: PyObject,
            event: &str,
            arg: PyObject,
            py: Python,
        ) -> Result<(), PyErr> {
            let user_code_call_site = match event {
                "call" => match self.call_frames.last() {
                    None => None,
                    Some((call_frame, call_frame_id)) => {
                        let pyframe = call_frame.cast_as::<PyFrame>(py)?;
                        Some(json!({
                            "call_frame_id": call_frame_id,
                            "line_number": pyframe.getattr("f_lineno")?.extract::<i32>()?,
                        }))
                    }
                },
                _ => None,
            };
            let pyframe = frame.cast_as::<PyFrame>(py)?;
            let arg = arg.cast_as::<PyAny>(py)?;
            let f_code = pyframe.getattr("f_code")?;
            let co_name = f_code.getattr("co_name")?;
            let name = co_name.extract::<String>()?;
            let pyframe_id = pyframe.as_ptr() as usize;
            let path = frame_path(pyframe)?;
            let qualname = get_qualname(pyframe, py)?;
            let locals = pyframe.getattr("f_locals")?;
            let json_locals = dump_json(py, locals)?;

            match event {
                "call" => {
                    let frame_ulid = Ulid::new();
                    let frame_id = format!("frm_{}", frame_ulid.to_string());
                    self._frame_ids.insert(pyframe_id, frame_id);
                    let frame_id = format!("frm_{}", frame_ulid.to_string());
                    self.call_frames.push((frame, frame_id));
                }
                "return" => {
                    self.call_frames.pop();
                }
                _ => {}
            }

            let frame_data = json!({
                "path": path,
                "co_name": name,
                "qualname": qualname,
                "event": event,
                "frame_id": self._frame_ids.get(&pyframe_id),
                "arg": dump_json(py, arg)?,
                "locals": json_locals,
                "timestamp": timestamp(),
                "type": "frame",
                "user_code_call_site": user_code_call_site,
            });
            self.frames_of_interest.push(frame_data);
            Ok(())
        }

        fn process_include_frames(&self, filename: &str) -> bool {
            self.include_frames.iter().any(|p| filename.contains(p))
        }

        fn process_ignore_frames(&self, filename: &str) -> bool {
            self.ignore_frames.iter().any(|p| filename.contains(p))
        }

        fn profile(
            &mut self,
            frame: PyObject,
            arg: PyObject,
            event: &str,
            py: Python,
        ) -> Result<(), PyErr> {
            let pyframe = frame.as_ref(py);
            let pyframe = pyframe.downcast::<PyFrame>()?;
            let f_code = pyframe.getattr("f_code")?;
            let co_filename = f_code.getattr("co_filename")?;
            let filename = co_filename.extract::<String>()?;

            if self.process_include_frames(&filename) {
                self.process_frame(frame, event, arg, py)?;
                return Ok(());
            };

            if self.process_ignore_frames(&filename) {
                return Ok(());
            }

            let co_name = f_code.getattr("co_name")?;
            let name = co_name.extract::<String>()?;

            if process_default_include_frames(
                py, self, &frame, pyframe, event, &arg, &name, &filename,
            )? {
                return Ok(());
            }

            if process_default_ignore_frames(pyframe, &name, &filename)? {
                return Ok(());
            }

            self.process_frame(frame, event, arg, py)
        }
    }

    #[pyfunction]
    fn register_profiler(profiler: PyObject) -> Result<(), PyErr> {
        Python::with_gil(|py| {
            let py_profiler = profiler.as_ref(py);
            if py_profiler.is_callable() {
                let config = py_profiler.getattr("config")?;
                let filters = config.get_item("filters");
                let include_frames = match filters {
                    Ok(filters) => match filters.get_item("include_frames") {
                        Ok(include_frames) => include_frames.extract()?,
                        Err(_) => Vec::new(),
                    },
                    Err(_) => Vec::new(),
                };
                let ignore_frames = match filters {
                    Ok(filters) => match filters.get_item("ignore_frames") {
                        Ok(ignore_frames) => ignore_frames.extract()?,
                        Err(_) => Vec::new(),
                    },
                    Err(_) => Vec::new(),
                };
                let rust_profiler = KoloProfiler {
                    db_path: py_profiler.getattr("db_path")?.str()?.extract()?,
                    one_trace_per_test: py_profiler.getattr("one_trace_per_test")?.extract()?,
                    trace_id: py_profiler.getattr("trace_id")?.extract()?,
                    frames_of_interest: Vec::new(),
                    config: config.into(),
                    include_frames,
                    ignore_frames,
                    default_include_frames: py_profiler
                        .getattr("_default_include_frames")?
                        .extract()?,
                    call_frames: Vec::new(),
                    timestamp: timestamp(),
                    _frame_ids: HashMap::new(),
                    start_test_index: 0,
                };
                let py_rust_profiler = rust_profiler.into_py(py);
                py_profiler.setattr("rust_profiler", &py_rust_profiler)?;
                unsafe {
                    ffi::PyEval_SetProfile(Some(profile), py_rust_profiler.into_ptr());
                }
                Ok(())
            } else {
                Err(PyTypeError::new_err("profiler object is not callable"))
            }
        })
    }

    #[pymodule]
    fn _kolo(_py: Python, m: &PyModule) -> PyResult<()> {
        m.add_function(wrap_pyfunction!(register_profiler, m)?)?;
        Ok(())
    }
}

#[cfg(not(PyPy))]
pub use _kolo::*;
