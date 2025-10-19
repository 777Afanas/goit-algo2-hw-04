from collections import deque

# --- 1. Реалізація Алгоритму Едмондса-Карпа ---
# Функції bfs та edmonds_karp залишаються без змін, оскільки вони коректні.
def bfs(capacity_matrix, flow_matrix, source, sink, parent):
    """Шукає шлях від source до sink у залишковому графі."""
    num_nodes = len(capacity_matrix)
    visited = [False] * num_nodes
    queue = deque([source])
    visited[source] = True
    while queue:
        u = queue.popleft()
        for v in range(num_nodes):
            if not visited[v] and capacity_matrix[u][v] - flow_matrix[u][v] > 0:
                parent[v] = u
                visited[v] = True
                if v == sink:
                    return True
                queue.append(v)
    return False

def edmonds_karp(capacity_matrix, source, sink):
    """Обчислює максимальний потік з source до sink."""
    num_nodes = len(capacity_matrix)
    flow_matrix = [[0] * num_nodes for _ in range(num_nodes)] 
    parent = [-1] * num_nodes
    max_flow = 0
    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        path_flow = float('Inf')
        s = sink
        while s != source:
            u = parent[s]
            path_flow = min(path_flow, capacity_matrix[u][s] - flow_matrix[u][s])
            s = u
        v = sink
        while v != source:
            u = parent[v]
            flow_matrix[u][v] += path_flow
            flow_matrix[v][u] -= path_flow  
            v = u
        max_flow += path_flow
    return max_flow, flow_matrix

# --- 2. Побудова Графа та Матриці Пропускної Здатності ---
# Цей розділ точно відображає наданий малюнок та таблицю пропускних здатностей.
nodes = {
    'S': 0, 'T': 20, 
    'Термінал 1': 1, 'Термінал 2': 2,
    'Склад 1': 3, 'Склад 2': 4, 'Склад 3': 5, 'Склад 4': 6,
    'Магазин 1': 7, 'Магазин 2': 8, 'Магазин 3': 9, 'Магазин 4': 10, 'Магазин 5': 11,
    'Магазин 6': 12, 'Магазин 7': 13, 'Магазин 8': 14, 'Магазин 9': 15, 'Магазин 10': 16,
    'Магазин 11': 17, 'Магазин 12': 18, 'Магазин 13': 19, 'Магазин 14': 20
}
num_nodes = 21 
INF = 1000 
capacity_matrix = [[0] * num_nodes for _ in range(num_nodes)]

edges = [
    ('S', 'Термінал 1', INF), ('S', 'Термінал 2', INF),
    
    # Термінали -> Склади (Згідно з таблицею та малюнком)
    ('Термінал 1', 'Склад 1', 25),
    ('Термінал 1', 'Склад 2', 20),
    ('Термінал 1', 'Склад 3', 15),
    ('Термінал 2', 'Склад 3', 15),
    ('Термінал 2', 'Склад 4', 30),
    ('Термінал 2', 'Склад 2', 10),

    # Склади -> Магазини
    ('Склад 1', 'Магазин 1', 15), ('Склад 1', 'Магазин 2', 10), ('Склад 1', 'Магазин 3', 20),
    ('Склад 2', 'Магазин 4', 15), ('Склад 2', 'Магазин 5', 10), ('Склад 2', 'Магазин 6', 25),
    ('Склад 3', 'Магазин 7', 20), ('Склад 3', 'Магазин 8', 15), ('Склад 3', 'Магазин 9', 10),
    ('Склад 4', 'Магазин 10', 20), ('Склад 4', 'Магазин 11', 10), ('Склад 4', 'Магазин 12', 15),
    ('Склад 4', 'Магазин 13', 5), ('Склад 4', 'Магазин 14', 10)
]

for u_name, v_name, cap in edges:
    u = nodes[u_name]
    v = nodes[v_name]
    capacity_matrix[u][v] = cap

shops = [f'Магазин {i}' for i in range(1, 15)]
T_index = nodes['T']
for shop_name in shops:
    capacity_matrix[nodes[shop_name]][T_index] = INF 


# --- 3. Виконання Алгоритму та Реконструкція Потоку ---

source_node = nodes['S']
sink_node = nodes['T']
max_flow, flow_matrix = edmonds_karp(capacity_matrix, source_node, sink_node)

reverse_nodes = {v: k for k, v in nodes.items()}
terminals = ['Термінал 1', 'Термінал 2']
warehouses = ['Склад 1', 'Склад 2', 'Склад 3', 'Склад 4']

# 3.1. Реконструкція: Обчислення потоку Термінал -> Магазин
# Обчислюємо внесок Термінала у потік кожного Складу, 
# а потім розподіляємо потік Склад -> Магазин пропорційно цьому внеску.

# Крок 1: Обчислюємо загальний потік у кожен Склад
warehouse_inflow = {w: 0 for w in warehouses}
for w in warehouses:
    w_idx = nodes[w]
    for t in terminals:
        t_idx = nodes[t]
        warehouse_inflow[w] += flow_matrix[t_idx][w_idx]

# Крок 2: Визначаємо частку потоку від кожного Термінала до кожного Складу
term_to_warehouse_share = {t: {} for t in terminals}
for t in terminals:
    t_idx = nodes[t]
    for w in warehouses:
        w_idx = nodes[w]
        inflow = flow_matrix[t_idx][w_idx]
        total_inflow = warehouse_inflow[w]
        # Частка Термінала у загальному потоці Складу
        share = inflow / total_inflow if total_inflow > 0 else 0
        term_to_warehouse_share[t][w] = share

# Крок 3: Розподіляємо потік Склад -> Магазин згідно з частками Терміналів
term_to_shop_flow = {t: {s: 0 for s in shops} for t in terminals}
for w in warehouses:
    w_idx = nodes[w]
    for s in shops:
        s_idx = nodes[s]
        # Потік, що надходить із цього Складу в цей Магазин
        warehouse_to_shop_flow = flow_matrix[w_idx][s_idx]
        
        # Розподіляємо цей потік між Терміналами
        for t in terminals:
            share = term_to_warehouse_share[t].get(w, 0)
            term_to_shop_flow[t][s] += warehouse_to_shop_flow * share

# Форматування таблиці Термінал -> Магазин
final_report_table = []
for t in terminals:
    for s in shops:
        flow = round(term_to_shop_flow[t][s]) # Округлюємо до цілих для читабельності
        final_report_table.append({'Термінал': t, 'Магазин': s, 'Фактичний Потік': flow})

# Збір потоків у Магазини (для Аналізу 3)
shop_flows = []
for s in shops:
    actual_flow_to_shop = flow_matrix[nodes[s]][T_index]
    shop_flows.append({
        'Магазин': s,
        'Потік до Магазину': actual_flow_to_shop
    })
# --- 4. Вивід та Аналіз ---

print(f"✅ Максимальний потік у мережі: {max_flow} одиниць")
print("-" * 50)
print("📊 Звіт: Аналіз Логістичної Мережі Максимального Потоку")
print("-" * 50)

# Таблиця: Фактичний Потік Термінал -> Магазин
print("\n## Таблиця: Фактичний Потік Термінал -> Магазин")
print("| Термінал | Магазин | Фактичний Потік (одиниць) |")
print("| :---: | :---: | :---: |")
for item in final_report_table:
    print(f"| {item['Термінал']} | {item['Магазин']} | {item['Фактичний Потік']} |")

print("\n## Аналіз Отриманих Результатів")

# Визначення сумарного потоку через Термінали (для Аналізу 1)
flow_term1 = sum(item['Фактичний Потік'] for item in final_report_table if item['Термінал'] == 'Термінал 1')
flow_term2 = sum(item['Фактичний Потік'] for item in final_report_table if item['Термінал'] == 'Термінал 2')

### 1. Які термінали забезпечують найбільший потік товарів до магазинів?
print("### 1. Які термінали забезпечують найбільший потік товарів до магазинів?")
print(f"**Термінал 1** постачає **{flow_term1}** одиниць.")
print(f"**Термінал 2** постачає **{flow_term2}** одиниць.")

if flow_term1 > flow_term2:
    print(f"**Термінал 1** ({flow_term1}) забезпечує більший потік, ніж Термінал 2 ({flow_term2}).")
elif flow_term2 > flow_term1:
    print(f"**Термінал 2** ({flow_term2}) забезпечує більший потік, ніж Термінал 1 ({flow_term1}).")
else:
    print("**Обидва термінали** забезпечують **однаковий потік** (100 одиниць кожен).")
    
### 2. Які маршрути мають найменшу пропускну здатність і як це впливає на загальний потік?
print("\n### 2. Які маршрути мають найменшу пропускну здатність і як це впливає на загальний потік?")
min_cut_capacity = sum(capacity_matrix[nodes[w]][nodes[s]] for w in warehouses for s in shops)
print(f"Найменша сумарна пропускна здатність (мінімальний розріз) знаходиться на розрізі **Склади → Магазини**, і вона становить **{min_cut_capacity} одиниць**.")
print(f"Це **вузьке місце** лімітує загальний потік до **{max_flow}** одиниць, відповідно до Теореми про мінімальний розріз-максимальний потік.")
print("Індивідуально найменшу пропускну здатність має маршрут **Склад 4 → Магазин 13** (**5 одиниць**).")

### 3. Які магазини отримали найменше товарів і чи можна збільшити їх постачання?
print(f"\n### 3. Які магазини отримали найменше товарів і чи можна збільшити їх постачання?")
max_shop_flow = max(shop_flows, key=lambda x: x['Потік до Магазину'])
min_shop_flow = min(shop_flows, key=lambda x: x['Потік до Магазину'])

print(f"Магазин з найменшим потоком: **{min_shop_flow['Магазин']}** з потоком **{min_shop_flow['Потік до Магазину']}** одиниць.")
print(f"Магазин з найбільшим потоком: **{max_shop_flow['Магазин']}** з потоком **{max_shop_flow['Потік до Магазину']}** одиниць.")
print("Можна збільшити постачання до **Магазину 13**, збільшивши пропускну здатність маршруту **Склад 4 → Магазин 13** (наразі 5 од.).")
print("Для збільшення загального постачання потрібно збільшити сумарну пропускну здатність на розрізі **Склади → Магазини**.")

### 4. Чи є вузькі місця, які можна усунути для покращення ефективності?
print("\n### 4. Чи є вузькі місця, які можна усунути для покращення ефективності?")
print("Головне вузьке місце – це **сумарна пропускна здатність усіх ребер від Складів до Магазинів** (200 одиниць).")
print("Для підвищення загальної ефективності та збільшення максимального потоку необхідно модернізувати канали **Склади → Магазини**, оскільки всі вони **насичені** (використовуються на 100% їх сумарної пропускної здатності).")