# base94 🚀

基于PyO3的高性能Base94编码/解码Rust实现，比原生Python版本快14-40倍。

## 特性

- ⚡ **极速处理**：使用Rust优化核心算法
- 🔄 **无缝兼容**：完美兼容纯Python版本
- 🛡️ **内存安全**：零拷贝操作与预分配缓冲区
- 📦 **简单API**：`b94encode`/`b94decode` 两个直观函数

## 安装

### 前置要求

- Rust工具链 (1.74+)
- Python 3.8+
- maturin (`pip install maturin`)

### 安装步骤

## pip 安装

```bash
# 安装稳定版本
pip install 'base94-rs'

# 安装测试版本
pip install git+https://github.com/hibays/base94.git
```

## 从源码编译

```bash
# 克隆仓库
git clone https://github.com/hibays/base94.git
cd base94

# 编译安装
pip install .
```

## 使用示例

```python
import base94

# 编码示例
data = b"Hello Base94!"
encoded = base94.b94encode(data)
print(f"Encoded: {encoded}")  # b'4Tk7J#qZcjYw'

# 解码示例
decoded = base94.b94decode(encoded)
print(f"Decoded: {decoded}")  # b'Hello Base94!'
```

## 性能对比

| 数据大小 | 实现版本         | 编码时间 (s) | 解码时间 (s) | 编码速度   | 解码速度   |
|----------|------------------|--------------|--------------|------------|------------|
| 10KB     | Python Native    |       0.0088 |       0.0067 | 1.11 MB/s  | 1.45 MB/s  |
| 10KB     | Rust Accelerated |       0.0003 |       0.0001 | 31.75 MB/s | 70.26 MB/s |
| 100KB    | Python Native    |       0.0523 |       0.0704 | 1.87 MB/s  | 1.39 MB/s  |
| 100KB    | Rust Accelerated |       0.0035 |       0.0014 | 28.13 MB/s | 72.17 MB/s |
| 1MB      | Python Native    |       0.5254 |       0.7434 | 1.90 MB/s  | 1.35 MB/s  |
| 1MB      | Rust Accelerated |       0.0388 |       0.0220 | 25.79 MB/s | 45.54 MB/s |
| 10MB     | Python Native    |       5.5060 |       7.6613 | 1.82 MB/s  | 1.31 MB/s  |
| 10MB     | Rust Accelerated |       0.3819 |       0.2030 | 26.19 MB/s | 49.27 MB/s |

> 测试环境：i7-13620H @ 2.4GHz, 32GB DDR5 RAM

## 技术细节

### 核心优化

- **查找表预计算**：使用`lazy_static`加速字符映射
- **SIMD内存布局**：对齐内存访问模式
- **块级并行**：9字节编码块的无锁处理
- **零堆分配**：完全栈内存操作

### 编码流程

```mermaid
graph TD
    %% 编码流程开始
    A[输入字节流] --> B{填充处理}
    B -->|补零| C[分块处理 9bytes/chunk]
    C --> D[转换为128位整数]
    D --> E[基数94分解]
    E --> F[查表编码]
    F --> G[输出Base94字符串]

    %% Python Binding 部分
    H[Python调用b94encode] --> I{自动选择实现}
    I -->|Python Native| J[py_b94encode]
    I -->|Rust Accelerated| K[rs_b94encode]

    %% 编码算法及加速细节
    L[查找表预计算] --> M[SIMD内存布局]
    M --> N[块级并行]
    N --> O[零堆分配]
    O --> G

    %% 编码最终结果
    G --> P[编码最终结果]

    %% 解码流程开始
    Q[输入Base94字符串] --> R{填充处理}
    R -->|补零| S[分块处理 11bytes/chunk]
    S --> T[Base94字符映射]
    T --> U[组合成9字节]
    U --> V[输出解码字节流]

    %% Python Binding 部分
    W[Python调用b94decode] --> X{自动选择实现}
    X -->|Python Native| Y[py_b94decode]
    X -->|Rust Accelerated| Z[rs_b94decode]

    %% 解码算法及加速细节
    AA[查找表预计算] --> BB[SIMD内存布局]
    BB --> CC[块级并行]
    CC --> DD[零堆分配]
    DD --> V

    %% 解码最终结果
    V --> EE[解码最终结果]
```

## 基准测试

```bash
# 运行单元测试
python -m pytest

# 运行性能测试
python -m python.benchmarks
```

## 本地开发

> 建议使用`uv`管理虚拟环境

```bash
# 创建虚拟环境
uv venv
# 安装依赖
uv pip install maturin twine
# 打包发布
uv build && twine upload dist/*
# 本地测试性安装
maturin develop --release
```

## 贡献指南

欢迎提交PR！建议流程：

1. Fork仓库
2. 创建特性分支 (`git checkout -b feature`)
3. 提交修改 (`git commit -am 'Add feature'`)
4. 推送到分支 (`git push origin feature`)
5. 创建Pull Request

## 许可证

[GPLv3](LICENSE)
