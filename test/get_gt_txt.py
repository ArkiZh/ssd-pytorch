# ----------------------------------------------------#
#   获取测试集的ground-truth
# ----------------------------------------------------#
import os

# TODO 要预测新模型，需要修改这里
validate_path = '../dataset/TLR2009_validate.txt'
label_name_path = "../dataset/TLR2009_label.txt"

with open(validate_path, mode="r", encoding="utf-8") as f:
    image_info =[line for line in f.read().strip().split("\n")]
with open(label_name_path, mode="r", encoding="utf-8") as f:
    labels = f.read().strip().split()

if not os.path.exists("./input"):
    os.makedirs("./input")
if not os.path.exists("./input/ground-truth"):
    os.makedirs("./input/ground-truth")

for i_info in image_info:
    info = i_info.split(" ")
    img_name = os.path.basename(info[0])
    with open("./input/ground-truth/{}.txt".format(img_name), mode="w+", encoding="utf-8") as f:
        for c in info[1:]:
            cc = c.split(",")
            f.write("{} {} {} {} {}\n".format(*[labels[int(cc[-1])]]+cc[:-1]))

print("Conversion completed!")
