"""Performance benchmark script"""

import time
from collections.abc import Callable
from dataclasses import dataclass

from src.cache.redis import RedisCache
from src.config import PostgresConfig, RedisConfig
from src.repositories.postgres import PostgresUserRepository
from src.services.user_service import UserService

DEFAULT_ITERATIONS = 100
USER_ID_RANGE = 100
MIN_USER_ID = 1
SEPARATOR_LENGTH = 50


@dataclass
class BenchmarkResult:
    test_name: str
    total_time: float
    iterations: int

    @property
    def average_time_ms(self) -> float:
        return (self.total_time / self.iterations) * 1000

    def relative_performance(self, baseline: float) -> float:
        return self.total_time / baseline if baseline > 0 else 0.0


class BenchmarkRunner:
    def __init__(
        self, service: UserService, cache: RedisCache, iterations: int = DEFAULT_ITERATIONS
    ):
        self.service = service
        self.cache = cache
        self.iterations = iterations

    def _calculate_user_id(self, iteration: int) -> int:
        return (iteration % USER_ID_RANGE) + MIN_USER_ID

    def _measure_execution_time(
        self, operation: Callable[[int], None], clear_cache: bool = False
    ) -> float:
        if clear_cache:
            self.cache.clear()

        start_time = time.time()
        for i in range(self.iterations):
            user_id = self._calculate_user_id(i)
            operation(user_id)
        return time.time() - start_time

    def run_postgres_benchmark(self) -> BenchmarkResult:
        total_time = self._measure_execution_time(
            lambda uid: self.service.get_user_by_id(uid, use_cache=False)
        )
        return BenchmarkResult("PostgreSQL直接アクセス", total_time, self.iterations)

    def run_cache_miss_benchmark(self) -> BenchmarkResult:
        total_time = self._measure_execution_time(
            lambda uid: self.service.get_user_by_id(uid, use_cache=True), clear_cache=True
        )
        return BenchmarkResult("キャッシュミス（初回）", total_time, self.iterations)

    def run_cache_hit_benchmark(self) -> BenchmarkResult:
        total_time = self._measure_execution_time(
            lambda uid: self.service.get_user_by_id(uid, use_cache=True)
        )
        return BenchmarkResult("キャッシュヒット（2回目）", total_time, self.iterations)


class BenchmarkReporter:
    @staticmethod
    def print_separator() -> None:
        print("=" * SEPARATOR_LENGTH)

    @staticmethod
    def print_header(iterations: int) -> None:
        print("Redis vs PostgreSQL パフォーマンス比較\n")
        print(f"テスト回数: {iterations}回\n")

    @staticmethod
    def print_initialization_success() -> None:
        print("サービス初期化成功\n")

    @staticmethod
    def print_cache_cleared() -> None:
        print("キャッシュをクリアしました\n")

    @staticmethod
    def print_test_result(test_number: int, result: BenchmarkResult) -> None:
        BenchmarkReporter.print_separator()
        print(f"テスト{test_number}: {result.test_name}")
        BenchmarkReporter.print_separator()
        print(f"実行時間: {result.total_time:.4f}秒")
        print(f"平均: {result.average_time_ms:.2f}ms/回\n")

    @staticmethod
    def print_summary(
        postgres_result: BenchmarkResult,
        cache_miss_result: BenchmarkResult,
        cache_hit_result: BenchmarkResult,
    ) -> None:
        BenchmarkReporter.print_separator()
        print("結果サマリ")
        BenchmarkReporter.print_separator()

        baseline = postgres_result.total_time
        print(f"PostgreSQL直接:           {postgres_result.total_time:.4f}秒 (基準)")
        print(
            f"キャッシュミス（初回）:    {cache_miss_result.total_time:.4f}秒 "
            f"({cache_miss_result.relative_performance(baseline):.2f}x)"
        )
        print(
            f"キャッシュヒット（2回目）: {cache_hit_result.total_time:.4f}秒 "
            f"({cache_hit_result.relative_performance(baseline):.2f}x)"
        )

        if cache_hit_result.total_time > 0:
            speedup = baseline / cache_hit_result.total_time
            print(f"\n速度向上: {speedup:.1f}倍高速")


def run_benchmark(iterations: int = DEFAULT_ITERATIONS) -> None:
    reporter = BenchmarkReporter()
    reporter.print_header(iterations)

    redis_config = RedisConfig()
    postgres_config = PostgresConfig()
    cache = RedisCache(redis_config)
    repository = PostgresUserRepository(postgres_config)
    service = UserService(repository, cache, redis_config)

    reporter.print_initialization_success()

    cache.clear()
    reporter.print_cache_cleared()

    runner = BenchmarkRunner(service, cache, iterations)

    postgres_result = runner.run_postgres_benchmark()
    reporter.print_test_result(1, postgres_result)

    cache_miss_result = runner.run_cache_miss_benchmark()
    reporter.print_test_result(2, cache_miss_result)

    cache_hit_result = runner.run_cache_hit_benchmark()
    reporter.print_test_result(3, cache_hit_result)

    reporter.print_summary(postgres_result, cache_miss_result, cache_hit_result)


if __name__ == "__main__":
    try:
        run_benchmark()
    except KeyboardInterrupt:
        print("\nベンチマークが中断されました")
    except ConnectionError as e:
        print(f"接続エラー: {e}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        raise
