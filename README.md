# Taobao image search

## How to use
1. Install requirements
```python
pip install -r requirements.txt
```

2. Change input querys in `input_querys.yaml`
3. Run script
```python
python run.py
python run.py --wait-int 5 # wait 5 seconds for each page
```

## Outputs
```bash
.
├── files
│    ├──{file_name}.tsv
├── images
│    ├──{file_name}
│    │      ├── {image_name1}.png
│    │      ├── {image_name2}.png
└──  └──    └──  ....png
 ```
