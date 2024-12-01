# comparación firma lenta y con TCR
from BlockChain import rsa_key
import time
import random
import pandas as pd
import matplotlib.pyplot as plt

random.seed(373)

def plot_table(results_sf, results_ss, n_bits, filename="comparison_plot.png"):
    """
    Genera un gráfico comparativo entre los tiempos de firma rápida y firma lenta.
    """
    df = pd.DataFrame({
        "Bits del Módulo": n_bits,
        "Tiempo Firma Rápida (s)": [results_sf[n] for n in n_bits],
        "Tiempo Firma Lenta (s)": [results_ss[n] for n in n_bits],
        "Ratio Mejora": [results_ss[n]/results_sf[n] for n in n_bits]
    })

    print(df)

    plt.figure(figsize=(10, 6))
    plt.plot(n_bits, df["Tiempo Firma Rápida (s)"], label="Firma Rápida (TCR)", marker='o')
    plt.plot(n_bits, df["Tiempo Firma Lenta (s)"], label="Firma Lenta", marker='o')
    plt.xlabel("Bits del Módulo")
    plt.ylabel("Tiempo (segundos)")
    plt.title("Comparación de Tiempos: Firma Rápida vs Firma Lenta")
    plt.legend()
    plt.grid()
    plt.show()

    # plt.savefig(filename)
    plt.close()

def create_data(n_bits, messages):
    results_sf = {n:0 for n in n_bits}
    results_ss = {n:0 for n in n_bits}
    
    for i, n in enumerate(n_bits):
        rsa = rsa_key(bits_modulo=n)
        print(f"n:{n}!!!")
        for m in messages: 
            start_sf = time.time()
            f1 = rsa.sign(m)
            sf = time.time() - start_sf

            start_ss = time.time()
            f2 = rsa.sign_slow(m)
            ss = time.time() - start_ss

            print(ss, sf)
            if f1 != f2:
                raise AssertionError("f1 != f2")
            
            results_sf[n] += sf
            results_ss[n] += ss

    # for n in n_bits:
    #     results_sf[n] /= len(messages)
    #     results_ss[n] /= len(messages)

    return results_sf, results_ss

if __name__=="__main__":
    # 512, 1024, 2048 y 4096
    n_bits = [512, 1024, 2048, 4096]
    messages = [random.randint(2**(4096-1), 2**4096 - 1) for _ in range(100) for n in n_bits]  # generated via random
    results_sf, results_ss = create_data(n_bits, messages)
    plot_table(results_sf, results_ss, n_bits)
    
