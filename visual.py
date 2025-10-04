import json
import networkx as nx
from pyvis.network import Network

# 1️⃣ Carregar o JSON do grafo
with open("osrs_graph.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 2️⃣ Criar grafo direcionado
G = nx.DiGraph()

# Adicionar nós com metadados
for node_id, node_info in data.items():
    G.add_node(node_id,
               name=node_info["name"],
               links_to=node_info["links_to"],
               linked_by=node_info["linked_by"])

# Adicionar arestas
for node_id, node_info in data.items():
    for target_id in node_info["links_to"]:
        if target_id in G.nodes:
            G.add_edge(node_id, target_id)

# 3️⃣ Criar visualização com Pyvis
net = Network(notebook=False, directed=True, height="800px", width="100%")
net.from_nx(G)

# Personalizar cores e títulos
for node_id in net.nodes:
    node_id_value = node_id["id"]
    node_data = G.nodes[node_id_value]
    node_id["title"] = f"Links to: {len(node_data['links_to'])}<br>Linked by: {len(node_data['linked_by'])}"
    node_id["label"] = node_data["name"]
    node_id["color"] = "#1f78b4" if len(node_data['links_to']) > 5 else "#33a02c"

net.toggle_physics(False)
# 4️⃣ Salvar em HTML e abrir
net.write_html("osrs_graph_visual.html")
print("Arquivo osrs_graph_visual.html gerado com sucesso! Abra no navegador para ver o grafo.")
