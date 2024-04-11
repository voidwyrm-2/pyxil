from pathlib import Path
from PIL import Image, UnidentifiedImageError
import argparse
import os

'''
   Copyright 2024 Nuclear Pasta

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''



parser = argparse.ArgumentParser()

parser.add_argument('path')

args = parser.parse_args()


path = Path(args.path)

if not path.exists(): print(f'path "{path}" does not exist'); raise SystemExit()


try: opened = Image.open(path)
except UnidentifiedImageError as e: print('unknown image format'); print('actual error:'); print(e)
colors = opened.getcolors()
size_x, size_y = opened.size
opened.close()

#print(colors)

colors = sorted(colors,key=lambda x: x[1][0] + x[1][1] + x[1][2] + x[1][3], reverse=True)


out = f'{size_x}-{size_y}\n'

for c in colors: out += f'{c[1][0]}, {c[1][1]}, {c[1][2]}\n'
out = out.strip()


print('what do you want to name the palette?')
print('it can\'t be empty and it can\'t have spaces')
while True:
    name = input('> ').strip().replace('\n', '').replace('/', '').replace('\\', '')
    if ' ' in name: print('name can\'t have spaces!'); continue
    if not name: print('name can\'t be empty!'); continue
    name = Path('./palettes', name.removesuffix('.pypal') + '.pypal')
    if name.exists():
        while True:
            reply = input(f'palette "{name}" already exists, do you want to overwrite it?(y/n)\n')
            match reply:
                case 'y': os.remove(name); break
                case 'n': raise SystemExit()
                case x: continue
    break


with open(name, 'xt') as pal:
    pal.write(out)