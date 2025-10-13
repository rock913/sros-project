#!/bin/bash

# VS Code Extension API Client Test
# Tests the extension's api.ts wrapper functions

set -e

BASE_URL="http://localhost:8121"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                               ║${NC}"
echo -e "${BLUE}║         VS Code Extension API Client Test                    ║${NC}"
echo -e "${BLUE}║                                                               ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

PASSED=0
FAILED=0

test_api() {
    local name="$1"
    local endpoint="$2"
    local expected_field="$3"
    
    echo -n "  Testing: $name ... "
    
    if result=$(curl -s "$BASE_URL$endpoint"); then
        if echo "$result" | jq -e ".$expected_field" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ PASS${NC}"
            PASSED=$((PASSED + 1))
        else
            echo -e "${RED}✗ FAIL${NC} (field '$expected_field' not found)"
            echo "    Response: $result" | head -c 200
            FAILED=$((FAILED + 1))
        fi
    else
        echo -e "${RED}✗ FAIL${NC} (request failed)"
        FAILED=$((FAILED + 1))
    fi
}

echo -e "${YELLOW}📚 Testing api.ts Functions${NC}"
echo ""

# getAllPapers()
test_api "getAllPapers()" "/papers?limit=10" "papers"

# getAllPapers({session_id})
SESSION_ID=$(curl -s "$BASE_URL/papers?limit=1" | jq -r '.papers[0].session_id // empty')
if [[ -n "$SESSION_ID" ]]; then
    test_api "getAllPapers({session_id})" "/papers?session_id=$SESSION_ID" "papers"
else
    echo "  ${YELLOW}⚠ SKIP${NC}: No session for getAllPapers({session_id})"
fi

# getAllPapers({source})
test_api "getAllPapers({source})" "/papers?source=arxiv" "papers"

# getAllPapers({keyword})
test_api "getAllPapers({keyword})" "/papers?keyword=quantum" "papers"

# getPaperById()
PAPER_ID=$(curl -s "$BASE_URL/papers?limit=1" | jq -r '.papers[0].id // empty')
if [[ -n "$PAPER_ID" ]]; then
    test_api "getPaperById()" "/papers/$PAPER_ID" "id"
else
    echo "  ${YELLOW}⚠ SKIP${NC}: No paper for getPaperById()"
fi

# exportPapers() - BibTeX
echo -n "  Testing: exportPapers('bibtex') ... "
if curl -s "$BASE_URL/papers/export?format=bibtex&limit=2" | grep -q "@article"; then
    echo -e "${GREEN}✓ PASS${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "${RED}✗ FAIL${NC}"
    FAILED=$((FAILED + 1))
fi

# exportPapers() - RIS
echo -n "  Testing: exportPapers('ris') ... "
if curl -s "$BASE_URL/papers/export?format=ris&limit=2" | grep -q "TY  -"; then
    echo -e "${GREEN}✓ PASS${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "${RED}✗ FAIL${NC}"
    FAILED=$((FAILED + 1))
fi

# exportPapers() - JSON
test_api "exportPapers('json')" "/papers/export?format=json&limit=2" "."

# getAllReports()
test_api "getAllReports()" "/reports?limit=10" "reports"

# getAllReports({session_id})
REPORT_SESSION=$(curl -s "$BASE_URL/reports?limit=1" | jq -r '.reports[0].session_id // empty')
if [[ -n "$REPORT_SESSION" ]]; then
    test_api "getAllReports({session_id})" "/reports?session_id=$REPORT_SESSION" "reports"
else
    echo "  ${YELLOW}⚠ SKIP${NC}: No session for getAllReports({session_id})"
fi

# getReportById()
REPORT_ID=$(curl -s "$BASE_URL/reports?limit=1" | jq -r '.reports[0].id // empty')
if [[ -n "$REPORT_ID" ]]; then
    test_api "getReportById()" "/reports/$REPORT_ID" "id"
else
    echo "  ${YELLOW}⚠ SKIP${NC}: No report for getReportById()"
fi

# getLatestReport()
if [[ -n "$REPORT_SESSION" ]]; then
    test_api "getLatestReport()" "/sessions/$REPORT_SESSION/reports/latest" "id"
else
    echo "  ${YELLOW}⚠ SKIP${NC}: No session for getLatestReport()"
fi

# exportReport() - Markdown
if [[ -n "$REPORT_ID" ]]; then
    echo -n "  Testing: exportReport('markdown') ... "
    if curl -s "$BASE_URL/reports/$REPORT_ID/export?format=markdown" | grep -q "."; then
        echo -e "${GREEN}✓ PASS${NC}"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC}"
        FAILED=$((FAILED + 1))
    fi
else
    echo "  ${YELLOW}⚠ SKIP${NC}: No report for exportReport('markdown')"
fi

# exportReport() - HTML
if [[ -n "$REPORT_ID" ]]; then
    echo -n "  Testing: exportReport('html') ... "
    if curl -s "$BASE_URL/reports/$REPORT_ID/export?format=html" | grep -q "<!DOCTYPE html>"; then
        echo -e "${GREEN}✓ PASS${NC}"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC}"
        FAILED=$((FAILED + 1))
    fi
else
    echo "  ${YELLOW}⚠ SKIP${NC}: No report for exportReport('html')"
fi

# compareReports()
REPORT_IDS=$(curl -s "$BASE_URL/reports?limit=2" | jq -r '.reports | map(.id) | @csv' | tr -d '"')
if [[ $(echo "$REPORT_IDS" | tr ',' '\n' | wc -l) -eq 2 ]]; then
    REPORT_1=$(echo "$REPORT_IDS" | cut -d',' -f1)
    REPORT_2=$(echo "$REPORT_IDS" | cut -d',' -f2)
    test_api "compareReports()" "/reports/compare?report_id_1=$REPORT_1&report_id_2=$REPORT_2" "diff"
else
    echo "  ${YELLOW}⚠ SKIP${NC}: Need 2 reports for compareReports()"
fi

echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                   Extension API Summary                       ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "  Passed: $PASSED"
echo "  Failed: $FAILED"
echo ""

if [[ $FAILED -eq 0 ]]; then
    echo -e "${GREEN}✅ All extension API tests passed!${NC}"
    echo ""
    echo -e "${YELLOW}Ready for VS Code Extension Development Host testing (F5)${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed${NC}"
    exit 1
fi
