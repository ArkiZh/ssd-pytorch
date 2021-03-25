import os
from collections import OrderedDict
from sklearn.model_selection import train_test_split

TLR_path_gt = "E:/workspace/datasets/TLR2009/Lara_UrbanSeq1_GroundTruth_GT.txt"
TLR_path_img = "E:/workspace/datasets/TLR2009/Lara3D_UrbanSeq1_JPG"

test_size = 200
ds_path_train = "./TLR2009_train.txt"
ds_path_validate = "./TLR2009_validate.txt"
label_path = "./TLR2009_label.txt"

ds_lines = OrderedDict()
label_map = OrderedDict()

with open(file=TLR_path_gt, mode="r", encoding="utf-8") as f:
    while True:
        cur_line = f.readline()
        if cur_line.startswith("#") or cur_line == "\n":
            continue
        if cur_line == "":
            break
        # Timestamp / frameindex x1 y1 x2 y2 id 'type' 'subtype'
        elements = cur_line.split(" ")
        cur_img_path = os.path.join(TLR_path_img, "frame_{:>06}.jpg".format(elements[2]))
        if not os.path.exists(cur_img_path):
            continue
        label = cur_line[cur_line.index(" '")+1:-1]
        label = label.replace("'", "").replace(" ", "-")
        if label in label_map:
            label_id = label_map[label]
        else:
            label_id = str(len(label_map))
            label_map[label] = label_id
        x1, y1, x2, y2, _ = elements[3:8]
        cur_content = ",".join((x1, y1, x2, y2, label_id))
        if cur_img_path in ds_lines:
            ds_lines[cur_img_path] = ds_lines[cur_img_path] + " " + cur_content
        else:
            ds_lines[cur_img_path] = cur_content

ds_train, ds_validate = train_test_split(list(ds_lines.items()), random_state=0, shuffle=True, test_size=test_size)

with open(file=ds_path_train, mode="w+", encoding="utf-8") as f:
    for k, v in ds_train:
        f.write("{} {}\n".format(k, v))

with open(file=ds_path_validate, mode="w+", encoding="utf-8") as f:
    for k, v in ds_validate:
        f.write("{} {}\n".format(k, v))

with open(file=label_path, mode="w+", encoding="utf-8") as f:
    for k, v in label_map.items():
        f.write("{}\n".format(k))
