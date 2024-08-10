import re
import argparse


parser = argparse.ArgumentParser(description='Put figures in bed')
parser.add_argument('-i', '--input-md', type=str, help='input markdown file', required=True)
parser.add_argument('-o', '--output-md', type=str, help='output markdown file', default='output.md')
parser.add_argument('--post-name', type=str, help='post name')
parser.add_argument('--map-file', type=str, help='file containing mapping from image name to url',
                    default='sm_links.txt')

def put_figures_in_bed(input_md, output_md, post_name, mapping, mapping_type='smms'):
    # find patterns like ![Perf report of QEMU running h264](qemu-vector-hotspot2.png)
    # replace qemu-vector-hotspot2.png with https://shinezyy.github.io/ArchShineZ/post/nemu-v/qemu-vector-hotspot2.png
    pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')
    with open(input_md, 'r', encoding='utf-8') as f, open(output_md, 'w', encoding='utf-8') as out_f:
        whole_file = f.read()
        real_content = whole_file.split('---')[2:]
        real_content = '---'.join(real_content)
        for line in real_content.split('\n'):
            match = pattern.search(line)
            if match:
                img_name = match.group(2)
                if mapping_type == 'smms':
                    img_url = mapping[img_name]
                elif mapping_type == 'imgse':
                    origin_name = img_name
                    img_name = img_name.replace('.png', '')
                    img_name = img_name.replace('_', ' ')
                    img_name = img_name.replace('-', ' ')
                    img_url = mapping[img_name]
                line = line.replace(origin_name, img_url)
            out_f.write(line+'\n')
        

def get_mapping_smms(map_file) -> dict:
    # Example line of map file: ![nemu-tlb.png](https://s2.loli.net/2024/08/09/4NzlhbUKCF2WckG.png)
    mapping = {}

    pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')
    with open(map_file, 'r', encoding='utf-8') as f:
        for line in f:
            m = pattern.match(line)
            if m is not None:
                mapping[m.group(1)] = m.group(2)
    
    assert len(mapping)
    return mapping
            

def get_mapping_imgse(imgse_l1, imgse_l2) -> dict:
    imgse_mapping_l1 = {}
    imgse_mapping_l2 = {}

    with open(imgse_l1, 'r', encoding='utf-8') as f:
        for line in f:
            if '.png' in line:
                v = line.strip()
            elif 'Archshinez' in line:
                continue
            else:
                k = line.strip()
                imgse_mapping_l1[k] = v

    # Example line of map file: [![pASMlDg.png](https://s21.ax1x.com/2024/08/09/pASMlDg.png)](https://imgse.com/i/pASMlDg)
    pattern = re.compile(r'\[\!\[(.*?)\]\((.*?)\)\]\((.*?)\)')
    with open(imgse_l2, 'r', encoding='utf-8') as f:
        for line in f:
            m = pattern.match(line)
            if m is not None:
                imgse_mapping_l2[m.group(1)] = m.group(2)
    
    mapping = {}
    for k, v in imgse_mapping_l1.items():
        mapping[k] = imgse_mapping_l2[v]
        
    print(mapping)
    return mapping


if __name__ == '__main__':
    args = parser.parse_args()
    if args.post_name:
        post_name = args.post_name
    elif '/' in args.input_md:
        post_name = args.input_md.split('/')[-2]
    elif '\\' in args.input_md:
        post_name = args.input_md.split('\\')[-2]
    else:
        print('Cannot find post name implicitly, please specify it with --post-name')
        raise

    mapping = get_mapping_imgse('imgse-l1.txt', 'imgse-l2.txt')

    put_figures_in_bed(args.input_md, args.output_md, post_name=post_name, mapping=mapping, mapping_type='imgse')