from src.application.use_cases.send_metrics_use_case import SendPypiStatsUseCase
from src.application.utils.logger_module import logger, log_extra_info, LogStatus


if __name__ == "__main__":
    try:
        send_pypi_stats_use_case = SendPypiStatsUseCase()
    except Exception as e:
        logger.error(
            "Error Instance of SendPypiStatsUseCase",
            extra=log_extra_info(status=LogStatus.ERROR),
        )
    try:
        df, err = send_pypi_stats_use_case.get_stats()
        if err:
            logger.error(
                "Error Getting Stats from DW",
                extra=log_extra_info(status=LogStatus.ERROR),
            )
            raise Exception(str(err))
    except Exception as e:
        logger.error(
            "Error Getting Stats from DW", extra=log_extra_info(status=LogStatus.ERROR)
        )
        raise Exception(str(e))

    try:
        send_pypi_stats_use_case.send_stats(df=df)
    except Exception as e:
        logger.error(
            "Error Sending Stats to DataDog",
            extra=log_extra_info(status=LogStatus.ERROR),
        )
        raise Exception(str(e))
