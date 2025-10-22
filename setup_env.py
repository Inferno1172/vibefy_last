import os
import warnings
import logging

# Only set environment variables here to avoid importing heavy libs at import time.
# This prevents TensorFlow (or other heavy libs) from being imported during module import,
# which can block the Streamlit server from starting.
os.environ.setdefault('TF_ENABLE_ONEDNN_OPTS', '0')
os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL', '3')  # suppress TF INFO/WARNING logs
os.environ.setdefault('CUDA_VISIBLE_DEVICES', '-1')  # disable GPU for stability in dev

# Filter common noisy warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

# Minimal logging configuration for startup; does not import tensorflow
logger = logging.getLogger("vibefy_setup")
if not logger.handlers:
    fh = logging.FileHandler("vibefy_setup.log")
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
logger.setLevel(logging.INFO)
logger.info("setup_env: environment variables set; tensorflow import is deferred.")


def init_tensorflow():
    """
    Call this function only when you actually need TensorFlow. It performs a safe import
    and reduces the chance of blocking the Streamlit main thread during app startup.
    """
    try:
        import tensorflow as tf
        tf.get_logger().setLevel('ERROR')
        logger.info("TensorFlow imported successfully via init_tensorflow()")
        return tf
    except Exception as e:
        logger.exception("Failed to import TensorFlow in init_tensorflow()")
        raise