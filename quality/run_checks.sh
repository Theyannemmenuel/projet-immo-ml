#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PASS=0
FAIL=0
TARGET="ml/"

if [ ! -d "$TARGET" ]; then
    echo -e "${RED}✗ Dossier ml/ introuvable. Lance depuis la racine du projet.${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}   ANALYSE QUALITE DU CODE — Projet Immobilier ML${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""

echo -e "${YELLOW}[1/4] PYLINT — Style et bonnes pratiques...${NC}"
pylint_output=$(pylint $TARGET --output-format=text 2>&1)
pylint_score=$(echo "$pylint_output" | grep "Your code has been rated" | grep -oP '[0-9]+\.[0-9]+(?=/10)')
if [ -n "$pylint_score" ]; then
    score_int=$(echo "$pylint_score" | cut -d. -f1)
    if [ "$score_int" -ge 8 ]; then
        echo -e "${GREEN}✓ PASS — Score : $pylint_score/10${NC}"
        PASS=$((PASS+1))
    else
        echo -e "${RED}✗ FAIL — Score : $pylint_score/10 (objectif : 8/10)${NC}"
        echo "$pylint_output" | grep -E "^ml/" | head -10
        FAIL=$((FAIL+1))
    fi
else
    echo -e "${GREEN}✓ PASS — Aucun fichier à analyser${NC}"
    PASS=$((PASS+1))
fi

echo ""
echo -e "${YELLOW}[2/4] FLAKE8 — Linting syntaxique...${NC}"
flake8_output=$(flake8 $TARGET --max-line-length=100 2>&1)
if [ -z "$flake8_output" ]; then
    echo -e "${GREEN}✓ PASS — 0 erreur${NC}"
    PASS=$((PASS+1))
else
    flake8_count=$(echo "$flake8_output" | wc -l | tr -d ' ')
    echo -e "${RED}✗ FAIL — $flake8_count erreur(s)${NC}"
    echo "$flake8_output" | head -10
    FAIL=$((FAIL+1))
fi

echo ""
echo -e "${YELLOW}[3/4] BANDIT — Sécurité...${NC}"
bandit_output=$(bandit -r $TARGET -ll 2>&1)
bandit_issues=$(echo "$bandit_output" | grep -c "Issue:" || echo "0")
if [ "$bandit_issues" -eq 0 ]; then
    echo -e "${GREEN}✓ PASS — 0 alerte critique${NC}"
    PASS=$((PASS+1))
else
    echo -e "${RED}✗ FAIL — $bandit_issues alerte(s) critique(s)${NC}"
    echo "$bandit_output" | grep -A2 "Issue:" | head -15
    FAIL=$((FAIL+1))
fi

echo ""
echo -e "${YELLOW}[4/4] RADON — Complexité cyclomatique...${NC}"
radon_output=$(radon cc $TARGET -s -a 2>&1)
radon_grade=$(echo "$radon_output" | grep "Average complexity" | grep -oP '[A-F](?=\))')
if [ -n "$radon_grade" ]; then
    if [[ "$radon_grade" == "A" || "$radon_grade" == "B" ]]; then
        echo -e "${GREEN}✓ PASS — Grade : $radon_grade${NC}"
        PASS=$((PASS+1))
    else
        echo -e "${RED}✗ FAIL — Grade : $radon_grade (objectif : A ou B)${NC}"
        FAIL=$((FAIL+1))
    fi
else
    echo -e "${GREEN}✓ PASS — Aucune fonction complexe${NC}"
    PASS=$((PASS+1))
fi

echo ""
echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}   RÉSUMÉ${NC}"
echo -e "${BLUE}============================================================${NC}"
echo -e "${GREEN}✓ PASS : $PASS/4${NC}"
echo -e "${RED}✗ FAIL : $FAIL/4${NC}"
echo ""
if [ "$FAIL" -eq 0 ]; then
    echo -e "${GREEN}🎉 Tous les checks PASS — Code validé !${NC}"
    exit 0
else
    echo -e "${RED}⚠️  $FAIL check(s) échoué(s) — corriger et relancer${NC}"
    exit 1
fi
