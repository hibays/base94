import timeit
import os
import sys
from functools import partial

# 测试数据大小配置（单位：字节）
TEST_CASES = [
    ("10KB", 10*1024),
    ("100KB", 100*1024),
    ("1MB", 1024*1024),
    ("10MB", 10*1024*1024),
]

def verify_correctness(impl):
    """验证实现正确性"""
    test_data = b"Base94 Test String"
    try:
        encoded = impl['encode'](test_data)
        decoded = impl['decode'](encoded)
        assert decoded == test_data, "Decode result mismatch"
    except Exception as e:
        print(f"⚠️ {impl['name']} 实现验证失败: {str(e)}")
        sys.exit(1)

def run_benchmark(impl, data):
    """执行单个基准测试"""
    results = {'encode': [], 'decode': []}
    
    # 预热缓存
    impl['encode'](data[:1024])
    impl['decode'](impl['encode'](data[:1024]))
    
    # 编码测试
    encode_timer = timeit.Timer(
        partial(impl['encode'], data),
        setup='gc.enable()'
    )
    results['encode'] = encode_timer.repeat(number=10, repeat=3)
    
    # 解码测试
    encoded_data = impl['encode'](data)
    decode_timer = timeit.Timer(
        partial(impl['decode'], encoded_data),
        setup='gc.enable()'
    )
    results['decode'] = decode_timer.repeat(number=10, repeat=3)
    
    return {
        'encode': min(results['encode']),
        'decode': min(results['decode'])
    }

def format_speed(bytes_size, seconds):
    """计算并格式化速度"""
    if seconds == 0:
        return "∞ MB/s"
    mb = bytes_size / (1024*1024)
    return f"{mb/seconds:.2f} MB/s"

def main():
    try:
        # 导入不同实现
        import base94
        
        implementations = [
            {
                'name': 'Python Native',
                'encode': base94.py_b94encode,
                'decode': base94.py_b94decode
            },
            {
                'name': 'Rust Accelerated',
                'encode': base94.rs_b94encode,
                'decode': base94.rs_b94decode
            }
        ]
        
        # 预先验证所有实现
        for impl in implementations:
            verify_correctness(impl)
        
        print("🚀 开始性能基准测试...\n")
        
        # 执行测试
        results = {}
        for case_name, data_size in TEST_CASES:
            print(f"\n🔧 生成测试数据: {case_name}...")
            data = os.urandom(data_size)
            results[case_name] = []
            
            for impl in implementations:
                print(f"🔍 测试 {impl['name']} ({case_name})...")
                try:
                    stats = run_benchmark(impl, data)
                    results[case_name].append({
                        'name': impl['name'],
                        'encode_time': stats['encode'],
                        'decode_time': stats['decode'],
                        'encode_speed': format_speed(data_size, stats['encode']),
                        'decode_speed': format_speed(data_size, stats['decode'])
                    })
                except MemoryError:
                    print(f"❌ 内存不足，跳过 {case_name} 测试")
                    continue
        
        # 打印结果表格
        print("\n📊 测试结果汇总:")
        print("| 数据大小 | 实现版本         | 编码时间 (s) | 解码时间 (s) | 编码速度   | 解码速度   |")
        print("|----------|------------------|--------------|--------------|------------|------------|")
        for case in TEST_CASES:
            case_name = case[0]
            for result in results.get(case_name, []):
                print(f"| {case_name:8} | {result['name']:16} | "
                      f"{result['encode_time']:12.4f} | {result['decode_time']:12.4f} | "
                      f"{result['encode_speed']:10} | {result['decode_speed']:10} |")
        
        # 打印性能提升比例
        print("\n💹 性能提升比例:")
        for case in TEST_CASES:
            case_name = case[0]
            if len(results.get(case_name, [])) == 2:
                py = results[case_name][0]
                rs = results[case_name][1]
                encode_ratio = py['encode_time'] / rs['encode_time']
                decode_ratio = py['decode_time'] / rs['decode_time']
                print(f"{case_name}:")
                print(f"  编码速度提升: {encode_ratio:.1f}x")
                print(f"  解码速度提升: {decode_ratio:.1f}x")
        
    except ImportError as e:
        print(f"❌ 导入错误: {str(e)}")
        print("请确保已正确安装：")
        print("1. Python原生版本: pip install base94")
        print("2. Rust加速版本: maturin develop --release")
        sys.exit(1)

if __name__ == "__main__":
    main()