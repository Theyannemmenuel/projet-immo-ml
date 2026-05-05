#!/bin/bash

echo "============================================"
echo "  DEPLOIEMENT RESEAU SDN - ContainerLab"
echo "  ESGI Toulouse - SRCC 2025-2026"
echo "============================================"

cd "$(dirname "$0")"

echo "🔨 Déploiement de la topologie SDN..."
sudo containerlab deploy -t topology.yml

echo ""
echo "✅ Réseau SDN déployé !"
echo "Noeuds actifs :"
sudo containerlab inspect -t topology.yml
