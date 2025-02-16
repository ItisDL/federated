package(default_visibility = ["//visibility:public"])

licenses(["notice"])  # Apache 2.0

# NOTE: TFF code outside this directory can depend on libraries defined in this
# directory, but not the other way round. In particular, utility classes and
# functions that depend on interfaces defined in the Core API belong in `core`,
# and those that deal with TensorFlow belong in `tensorflow_libs`.

py_library(
    name = "common_libs",
    srcs = ["__init__.py"],
)

py_library(
    name = "anonymous_tuple",
    srcs = ["anonymous_tuple.py"],
    deps = [":py_typecheck"],
)

py_test(
    name = "anonymous_tuple_test",
    size = "small",
    srcs = ["anonymous_tuple_test.py"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = [":anonymous_tuple"],
)

py_library(
    name = "py_typecheck",
    srcs = ["py_typecheck.py"],
)

py_test(
    name = "py_typecheck_test",
    size = "small",
    srcs = ["py_typecheck_test.py"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = [
        ":anonymous_tuple",
        ":py_typecheck",
    ],
)

py_library(
    name = "serialization_utils",
    srcs = ["serialization_utils.py"],
    deps = [
        ":py_typecheck",
        "@com_google_protobuf//:protobuf_python",
    ],
)

py_test(
    name = "serialization_utils_test",
    size = "small",
    srcs = ["serialization_utils_test.py"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = [
        ":serialization_utils",
        "@com_google_protobuf//:protobuf_python",
    ],
)

py_library(
    name = "test",
    testonly = 1,
    srcs = ["test.py"],
)

py_test(
    name = "test_test",
    size = "small",
    srcs = ["test_test.py"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = [":test"],
)
