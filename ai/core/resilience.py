import asyncio
import time
import functools
import logging
from typing import Callable, Any, TypeVar, List

logger = logging.getLogger("Squad3_AI_Resilience")
logging.basicConfig(level=logging.INFO)

T = TypeVar("T")


def with_retry(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """
    Decorador de Resiliência com Exponential Backoff e Jitter.
    Suporta funções síncronas e assíncronas.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            delay = initial_delay
            last_exception = None

            for attempt in range(1, max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_retries:
                        logger.error(f"[Retry] Falha definitiva após {max_retries} tentativas no método '{func.__name__}': {e}")
                        raise e
                    
                    logger.warning(f"[Retry] Tentativa {attempt}/{max_retries} no método '{func.__name__}' falhou ({e}). Aguardando {delay:.2f}s...")
                    await asyncio.sleep(delay)
                    delay *= backoff_factor

            raise last_exception  # type: ignore

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            delay = initial_delay
            last_exception = None

            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_retries:
                        logger.error(f"[Retry] Falha definitiva após {max_retries} tentativas no método '{func.__name__}': {e}")
                        raise e

                    logger.warning(f"[Retry] Tentativa {attempt}/{max_retries} no método '{func.__name__}' falhou ({e}). Aguardando {delay:.2f}s...")
                    time.sleep(delay)
                    delay *= backoff_factor

            raise last_exception  # type: ignore

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator


def execute_with_fallback(
    primary_fn: Callable[[], T],
    fallback_fn: Callable[[], T],
    primary_name: str = "gemini-2.5-flash",
    fallback_name: str = "gemini-2.5-pro"
) -> T:
    """
    Executa primary_fn; em caso de erro de validação ou indisponibilidade,
    faz fallback automático para fallback_fn.
    """
    try:
        return primary_fn()
    except Exception as primary_error:
        logger.warning(f"[Fallback Cascade] Erro no modelo primário '{primary_name}': {primary_error}. Tentando modelo fallback '{fallback_name}'...")
        try:
            return fallback_fn()
        except Exception as fallback_error:
            logger.error(f"[Fallback Cascade] Erro também no modelo fallback '{fallback_name}': {fallback_error}")
            raise fallback_error
