from src.application.use_cases.send_metrics_use_case import SendPypiStatsUseCase

if __name__ == "__main__":
    send_pypi_stats_use_case = SendPypiStatsUseCase()
    print("Getting stats from DW...")
    df, err = send_pypi_stats_use_case.get_stats()
    print("Sending stats to DataDog...")
    send_pypi_stats_use_case.send_stats(df=df)
    print("Done!")
