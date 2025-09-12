# -*- coding: utf-8 -*-
from app.similarity import score, is_similar
import pandas as pd

ORIGINAL = 'Carrera 70 # 26A - 33'
THRESHOLD = 90

# 1) Homonimos generados por el pipeline
df = pd.read_csv('.\\workdir\\homonimos.csv')
good = df['homonimos'].tolist()

# 2) Casos "malos" que deberian NO pasar
bad = [
    'Carrera 71 # 26A - 33',       # cambia la via
    'Carrera 70 # 26B - 33',       # cambia la letra
    'Calle 70 # 26A - 33',         # cambia tipo de via
    'Carrera 70 # 26A - 330',      # cambia el numero final
    'Av 70 # 26A - 33, Bogota',    # cambia ciudad/contexto
]

all_cases = [('GOOD', a) for a in good] + [('BAD', b) for b in bad]

passed, failed = [], []
for tag, addr in all_cases:
    sc = score(ORIGINAL, addr)
    if is_similar(ORIGINAL, addr, threshold=THRESHOLD):
        passed.append((tag, addr, sc))
    else:
        failed.append((tag, addr, sc))

print(f'Umbral = {THRESHOLD}')
print(f'PASARON: {len(passed)} de {len(all_cases)}')
print(f'NO PASARON: {len(failed)}')

print('\n--- Ejemplos que PASAN ---')
for tag, addr, sc in passed[:10]:
    print(f'[{tag}] {addr}  -> score={sc:.1f}')

print('\n--- Ejemplos que NO PASAN ---')
for tag, addr, sc in failed:
    print(f'[{tag}] {addr}  -> score={sc:.1f}')
