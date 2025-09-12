import pandas as pd
for name in ['homonimos','homonimos_filtrados','resultados','resultados_unicos']:
    df = pd.read_csv(f'.\\\\workdir\\\\{name}.csv')
    print(f'--- {name}.csv (primeras 10 filas) ---')
    print(df.head(10).to_string(index=False))
    print()
