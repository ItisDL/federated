package(default_visibility = ["//tensorflow_federated/python/core:__subpackages__"])

licenses(["notice"])  # Apache 2.0

# This is the import for other components of TFF that are layered upon the Core
# utils.
py_library(
    name = "utils",
    srcs = ["__init__.py"],
    visibility = ["//visibility:public"],
    deps = [
        ":computation_utils",
        ":differential_privacy",
        ":encoding_utils",
        ":federated_aggregations",
        ":tf_computation_utils",
    ],
)

py_library(
    name = "computation_utils",
    srcs = ["computation_utils.py"],
    deps = [
        "//tensorflow_federated/python/common_libs:py_typecheck",
        "//tensorflow_federated/python/core/api",
    ],
)

py_test(
    name = "computation_utils_test",
    size = "small",
    srcs = ["computation_utils_test.py"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = [
        ":computation_utils",
        "//tensorflow_federated/python/core/api",
    ],
)

py_library(
    name = "differential_privacy",
    srcs = ["differential_privacy.py"],
    deps = [
        ":computation_utils",
        "//tensorflow_federated/python/core/api",
        "//tensorflow_federated/python/core/framework",
    ],
)

py_test(
    name = "differential_privacy_test",
    srcs = ["differential_privacy_test.py"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = [
        ":differential_privacy",
        "//tensorflow_federated/python/common_libs:test",
        "//tensorflow_federated/python/core/api",
        "//tensorflow_federated/python/core/framework",
    ],
)

py_library(
    name = "encoding_utils",
    srcs = ["encoding_utils.py"],
    deps = [
        ":computation_utils",
        "//tensorflow_federated/python/core/api",
        "//tensorflow_federated/python/core/framework",
        "//tensorflow_federated/python/tensorflow_libs:nest",
    ],
)

py_test(
    name = "encoding_utils_test",
    srcs = ["encoding_utils_test.py"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = [
        ":computation_utils",
        ":encoding_utils",
        "//tensorflow_federated/python/common_libs:test",
        "//tensorflow_federated/python/core/api",
    ],
)

py_library(
    name = "federated_aggregations",
    srcs = ["federated_aggregations.py"],
    deps = [
        "//tensorflow_federated/python/common_libs:anonymous_tuple",
        "//tensorflow_federated/python/common_libs:py_typecheck",
        "//tensorflow_federated/python/core/api",
    ],
)

py_test(
    name = "federated_aggregations_test",
    size = "small",
    srcs = ["federated_aggregations_test.py"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = [
        ":federated_aggregations",
        "//tensorflow_federated/python/core/api",
    ],
)

py_library(
    name = "test",
    srcs = ["test.py"],
    srcs_version = "PY3",
    deps = [
        "//tensorflow_federated/python/core/api:computations",
        "//tensorflow_federated/python/core/impl:executor_stacks",
        "//tensorflow_federated/python/core/impl:set_default_executor",
    ],
)

py_library(
    name = "tf_computation_utils",
    srcs = ["tf_computation_utils.py"],
    deps = [
        "//tensorflow_federated/python/common_libs:anonymous_tuple",
        "//tensorflow_federated/python/common_libs:py_typecheck",
        "//tensorflow_federated/python/core/api:computation_types",
    ],
)

py_test(
    name = "tf_computation_utils_test",
    size = "small",
    srcs = ["tf_computation_utils_test.py"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = [
        ":tf_computation_utils",
        "//tensorflow_federated/python/common_libs:anonymous_tuple",
        "//tensorflow_federated/python/common_libs:test",
    ],
)
