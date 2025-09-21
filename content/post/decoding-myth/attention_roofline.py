def mla(name, seq_len, head_num, head_dim, nope_dim, chunk_size, elem_size, o_size):
    qk_ops = seq_len * head_num * head_dim * chunk_size * 2
    pv_ops = seq_len * head_num * chunk_size * nope_dim * 2
    memory_bytes = seq_len * head_num * head_dim * elem_size + \
        head_dim * chunk_size * elem_size + \
        head_num * chunk_size * o_size

    compute_density = (qk_ops + pv_ops) / memory_bytes
    print(f"{name} compute_density: {compute_density:.3f}")
    return compute_density

def gqa(name, seq_len, q_head_num, kv_head_num, head_dim, chunk_size, elem_size, o_size):
    group_size = q_head_num // kv_head_num
    group_num = kv_head_num
    qk_ops = (seq_len * group_size * head_dim * chunk_size * 2) * group_num
    pv_ops = (seq_len * group_size * chunk_size * head_dim * 2) * group_num
    memory_bytes = seq_len * q_head_num * head_dim * elem_size + \
        2 * kv_head_num * head_dim * chunk_size * elem_size + \
        q_head_num * chunk_size * o_size

    compute_density = (qk_ops + pv_ops) / memory_bytes
    print(f"{name} compute_density: {compute_density:.3f}, group size * q_seq_len: {group_size * seq_len}")
    return compute_density
    
def h100():
    tflops = 989
    tB_per_sec = 3.35
    print(f"H100, compute density: {tflops / tB_per_sec:.3f}")
    return tflops / tB_per_sec

def h20():
    tflops = 148
    tB_per_sec = 4.0
    print(f"H20, compute density: {tflops / tB_per_sec:.3f}")
    return tflops / tB_per_sec

def ai_max_395():
    tflops = 50
    tB_per_sec = 0.25
    print(f"AI MAX 395, compute density: {tflops / tB_per_sec:.3f}")
    return tflops / tB_per_sec

def RTX5090():
    tflops = 209
    tB_per_sec = 1.79
    print(f"RTX 5090, compute density: {tflops / tB_per_sec:.3f}")
    return tflops / tB_per_sec

# 定义GQA配置
gqa_configs = [
    ("GQA qlen=1", 1),
    ("GQA qlen=4", 4), 
    ("GQA qlen=8", 8),
    ("GQA qlen=16", 16),
    ("GQA qlen=32", 32),
    ("GQA qlen=48", 48),
    ("GQA qlen=64", 64)
]

# 定义硬件配置
hardware_configs = [
    ("H20", h20),
    ("RTX 5090", RTX5090),
    ("AI MAX 395", ai_max_395), 
    ("H100", h100)
]

print("=" * 50)
print("Computing GQA configurations...")

# 计算所有GQA配置的计算访存比
gqa_densities = {}
for name, seq_len in gqa_configs:
    density = gqa(name, seq_len=seq_len, q_head_num=64, kv_head_num=8, head_dim=128, chunk_size=512, elem_size=2, o_size=2)
    gqa_densities[name] = density

print("\n" + "=" * 50)
print("Computing hardware specifications...")

# 计算所有硬件的计算访存比
hardware_densities = {}
for name, func in hardware_configs:
    density = func()
    hardware_densities[name] = density

print("\n" + "=" * 50)
print("Generating comparison table...\n")

# 生成Markdown表格
def generate_comparison_table():
    # 表头
    header = "| GQA Configuration |"
    for hw_name, _ in hardware_configs:
        header += f" {hw_name} |"
    
    # 分隔线
    separator = "|" + "---|" * (len(hardware_configs) + 1)
    
    print(header)
    print(separator)
    
    # 表格内容
    for gqa_name, _ in gqa_configs:
        row = f"| {gqa_name} |"
        gqa_density = gqa_densities[gqa_name]
        
        for hw_name, _ in hardware_configs:
            hw_density = hardware_densities[hw_name]
            
            # 判断是compute bound还是memory bound
            if gqa_density > hw_density:
                bound_type = "Compute Bound"
            else:
                bound_type = "Memory Bound"
            
            row += f" {bound_type} |"
        
        print(row)

generate_comparison_table()