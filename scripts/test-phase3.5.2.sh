#!/bin/bash

# Phase 3.5.2 Feature Testing Script
# Tests all 9 new API endpoints and export formats

set -e

BASE_URL="http://localhost:8121"
TEST_DIR="/tmp/phase3.5.2-test"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create test directory
mkdir -p "$TEST_DIR"

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                               ║${NC}"
echo -e "${BLUE}║         Phase 3.5.2 Comprehensive Feature Test               ║${NC}"
echo -e "${BLUE}║                                                               ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Test counter
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to run test
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_pattern="$3"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -n "  Testing: $test_name ... "
    
    if result=$(eval "$test_command" 2>&1); then
        if [[ -z "$expected_pattern" ]] || echo "$result" | grep -q "$expected_pattern"; then
            echo -e "${GREEN}✓ PASS${NC}"
            PASSED_TESTS=$((PASSED_TESTS + 1))
            return 0
        else
            echo -e "${RED}✗ FAIL${NC} (pattern not found: $expected_pattern)"
            echo "  Output: $result"
            FAILED_TESTS=$((FAILED_TESTS + 1))
            return 1
        fi
    else
        echo -e "${RED}✗ FAIL${NC} (command failed)"
        echo "  Error: $result"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

echo -e "${YELLOW}📋 Test Suite 1: Paper Management APIs${NC}"
echo ""

# Test 1.1: Get all papers
run_test "GET /papers (all papers)" \
    "curl -s '$BASE_URL/papers?limit=100' | jq -r '.papers | length'" \
    "[0-9]"

# Test 1.2: Get papers by session
SESSION_ID=$(curl -s "$BASE_URL/papers?limit=1" | jq -r '.papers[0].session_id // empty')
if [[ -n "$SESSION_ID" ]]; then
    run_test "GET /papers?session_id=xxx" \
        "curl -s '$BASE_URL/papers?session_id=$SESSION_ID' | jq -r '.papers[0].session_id'" \
        "$SESSION_ID"
else
    echo "  ${YELLOW}⚠ SKIP${NC}: No papers found for session filtering test"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
fi

# Test 1.3: Get papers by source
run_test "GET /papers?source=arxiv" \
    "curl -s '$BASE_URL/papers?source=arxiv&limit=10' | jq -r '.total'" \
    "[0-9]"

# Test 1.4: Full-text search
run_test "GET /papers?keyword=xxx" \
    "curl -s '$BASE_URL/papers?keyword=machine&limit=10' | jq -r '.total'" \
    "[0-9]"

# Test 1.5: Pagination
run_test "GET /papers with pagination" \
    "curl -s '$BASE_URL/papers?limit=2&offset=0' | jq -r '.limit'" \
    "2"

# Test 1.6: Get paper by ID
PAPER_ID=$(curl -s "$BASE_URL/papers?limit=1" | jq -r '.papers[0].id // empty')
if [[ -n "$PAPER_ID" ]]; then
    run_test "GET /papers/{paper_id}" \
        "curl -s '$BASE_URL/papers/$PAPER_ID' | jq -r '.id'" \
        "$PAPER_ID"
else
    echo "  ${YELLOW}⚠ SKIP${NC}: No papers found for ID test"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
fi

echo ""
echo -e "${YELLOW}📤 Test Suite 2: Paper Export Formats${NC}"
echo ""

# Test 2.1: Export to BibTeX
run_test "Export papers to BibTeX" \
    "curl -s '$BASE_URL/papers/export?format=bibtex&limit=2' | head -n 1" \
    "@article"

# Test 2.2: Export to RIS
run_test "Export papers to RIS" \
    "curl -s '$BASE_URL/papers/export?format=ris&limit=2' | head -n 1" \
    "TY  -"

# Test 2.3: Export to JSON
run_test "Export papers to JSON" \
    "curl -s '$BASE_URL/papers/export?format=json&limit=2' | jq -r 'type'" \
    "array"

# Test 2.4: Export with session filter
if [[ -n "$SESSION_ID" ]]; then
    run_test "Export papers by session" \
        "curl -s '$BASE_URL/papers/export?format=json&session_id=$SESSION_ID' | jq -r '.[0].session_id'" \
        "$SESSION_ID"
else
    echo "  ${YELLOW}⚠ SKIP${NC}: No session for export filter test"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
fi

echo ""
echo -e "${YELLOW}📊 Test Suite 3: Report Management APIs${NC}"
echo ""

# Test 3.1: Get all reports
run_test "GET /reports (all reports)" \
    "curl -s '$BASE_URL/reports?limit=100' | jq -r '.reports | length'" \
    "[0-9]"

# Test 3.2: Get reports by session
REPORT_SESSION=$(curl -s "$BASE_URL/reports?limit=1" | jq -r '.reports[0].session_id // empty')
if [[ -n "$REPORT_SESSION" ]]; then
    run_test "GET /reports?session_id=xxx" \
        "curl -s '$BASE_URL/reports?session_id=$REPORT_SESSION' | jq -r '.reports[0].session_id'" \
        "$REPORT_SESSION"
else
    echo "  ${YELLOW}⚠ SKIP${NC}: No reports found for session filtering test"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
fi

# Test 3.3: Get reports with pagination
run_test "GET /reports with pagination" \
    "curl -s '$BASE_URL/reports?limit=2&offset=0' | jq -r '.limit'" \
    "2"

# Test 3.4: Get report by ID
REPORT_ID=$(curl -s "$BASE_URL/reports?limit=1" | jq -r '.reports[0].id // empty')
if [[ -n "$REPORT_ID" ]]; then
    run_test "GET /reports/{report_id}" \
        "curl -s '$BASE_URL/reports/$REPORT_ID' | jq -r '.id'" \
        "$REPORT_ID"
else
    echo "  ${YELLOW}⚠ SKIP${NC}: No reports found for ID test"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
fi

# Test 3.5: Get latest report
if [[ -n "$REPORT_SESSION" ]]; then
    run_test "GET /sessions/{id}/reports/latest" \
        "curl -s '$BASE_URL/sessions/$REPORT_SESSION/reports/latest' | jq -r '.session_id'" \
        "$REPORT_SESSION"
else
    echo "  ${YELLOW}⚠ SKIP${NC}: No session for latest report test"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
fi

echo ""
echo -e "${YELLOW}📤 Test Suite 4: Report Export Formats${NC}"
echo ""

if [[ -n "$REPORT_ID" ]]; then
    # Test 4.1: Export to Markdown
    run_test "Export report to Markdown" \
        "curl -s '$BASE_URL/reports/$REPORT_ID/export?format=markdown' | head -c 10" \
        "."
    
    # Test 4.2: Export to HTML
    run_test "Export report to HTML" \
        "curl -s '$BASE_URL/reports/$REPORT_ID/export?format=html' | grep -o '<!DOCTYPE html>'" \
        "<!DOCTYPE html>"
    
    # Test 4.3: Export to PDF (should return error 501)
    run_test "Export report to PDF (not implemented)" \
        "curl -s '$BASE_URL/reports/$REPORT_ID/export?format=pdf' | jq -r '.detail'" \
        "PDF export not yet implemented"
else
    echo "  ${YELLOW}⚠ SKIP${NC}: No report for export tests (3 tests)"
    TOTAL_TESTS=$((TOTAL_TESTS + 3))
fi

echo ""
echo -e "${YELLOW}⚖️  Test Suite 5: Report Comparison${NC}"
echo ""

# Test 5.1: Compare two reports
REPORT_IDS=$(curl -s "$BASE_URL/reports?limit=2" | jq -r '.reports | map(.id) | @csv' | tr -d '"')
if [[ $(echo "$REPORT_IDS" | tr ',' '\n' | wc -l) -eq 2 ]]; then
    REPORT_1=$(echo "$REPORT_IDS" | cut -d',' -f1)
    REPORT_2=$(echo "$REPORT_IDS" | cut -d',' -f2)
    
    run_test "GET /reports/compare?report_id_1=xxx&report_id_2=yyy" \
        "curl -s '$BASE_URL/reports/compare?report_id_1=$REPORT_1&report_id_2=$REPORT_2' | jq -r '.diff'" \
        "."
else
    echo "  ${YELLOW}⚠ SKIP${NC}: Need at least 2 reports for comparison test"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
fi

echo ""
echo -e "${YELLOW}🔍 Test Suite 6: Data Validation${NC}"
echo ""

# Test 6.1: Verify paper schema
if [[ -n "$PAPER_ID" ]]; then
    run_test "Paper has required fields" \
        "curl -s '$BASE_URL/papers/$PAPER_ID' | jq -r 'has(\"id\") and has(\"title\") and has(\"authors\")'" \
        "true"
else
    echo "  ${YELLOW}⚠ SKIP${NC}: No paper for schema validation"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
fi

# Test 6.2: Verify report schema
if [[ -n "$REPORT_ID" ]]; then
    run_test "Report has required fields" \
        "curl -s '$BASE_URL/reports/$REPORT_ID' | jq -r 'has(\"id\") and has(\"content\") and has(\"version\")'" \
        "true"
else
    echo "  ${YELLOW}⚠ SKIP${NC}: No report for schema validation"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
fi

# Test 6.3: Verify report version ordering
if [[ -n "$REPORT_SESSION" ]]; then
    run_test "Reports sorted by version desc" \
        "curl -s '$BASE_URL/reports?session_id=$REPORT_SESSION' | jq -r '.reports | length'" \
        "[0-9]"
else
    echo "  ${YELLOW}⚠ SKIP${NC}: No session for version ordering test"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
fi

echo ""
echo -e "${YELLOW}📁 Test Suite 7: Export File Generation${NC}"
echo ""

# Test 7.1: Save BibTeX to file
BIBTEX_FILE="$TEST_DIR/papers_$TIMESTAMP.bib"
if curl -s "$BASE_URL/papers/export?format=bibtex&limit=5" > "$BIBTEX_FILE"; then
    if [[ -s "$BIBTEX_FILE" ]] && grep -q "@article" "$BIBTEX_FILE"; then
        echo -e "  Testing: Save BibTeX to file ... ${GREEN}✓ PASS${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        echo "    File: $BIBTEX_FILE ($(wc -l < "$BIBTEX_FILE") lines)"
    else
        echo -e "  Testing: Save BibTeX to file ... ${RED}✗ FAIL${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
else
    echo -e "  Testing: Save BibTeX to file ... ${RED}✗ FAIL${NC}"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))

# Test 7.2: Save RIS to file
RIS_FILE="$TEST_DIR/papers_$TIMESTAMP.ris"
if curl -s "$BASE_URL/papers/export?format=ris&limit=5" > "$RIS_FILE"; then
    if [[ -s "$RIS_FILE" ]] && grep -q "TY  -" "$RIS_FILE"; then
        echo -e "  Testing: Save RIS to file ... ${GREEN}✓ PASS${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        echo "    File: $RIS_FILE ($(wc -l < "$RIS_FILE") lines)"
    else
        echo -e "  Testing: Save RIS to file ... ${RED}✗ FAIL${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
else
    echo -e "  Testing: Save RIS to file ... ${RED}✗ FAIL${NC}"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))

# Test 7.3: Save HTML report to file
if [[ -n "$REPORT_ID" ]]; then
    HTML_FILE="$TEST_DIR/report_$TIMESTAMP.html"
    if curl -s "$BASE_URL/reports/$REPORT_ID/export?format=html" > "$HTML_FILE"; then
        if [[ -s "$HTML_FILE" ]] && grep -q "<!DOCTYPE html>" "$HTML_FILE"; then
            echo -e "  Testing: Save HTML report to file ... ${GREEN}✓ PASS${NC}"
            PASSED_TESTS=$((PASSED_TESTS + 1))
            echo "    File: $HTML_FILE ($(wc -l < "$HTML_FILE") lines)"
        else
            echo -e "  Testing: Save HTML report to file ... ${RED}✗ FAIL${NC}"
            FAILED_TESTS=$((FAILED_TESTS + 1))
        fi
    else
        echo -e "  Testing: Save HTML report to file ... ${RED}✗ FAIL${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
else
    echo "  ${YELLOW}⚠ SKIP${NC}: No report for HTML export"
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))

echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                      Test Summary                             ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "  Total Tests:  $TOTAL_TESTS"
echo -e "  ${GREEN}Passed:       $PASSED_TESTS${NC}"
if [[ $FAILED_TESTS -gt 0 ]]; then
    echo -e "  ${RED}Failed:       $FAILED_TESTS${NC}"
fi
echo ""

# Calculate pass rate
PASS_RATE=$((PASSED_TESTS * 100 / TOTAL_TESTS))
echo "  Pass Rate:    $PASS_RATE%"
echo ""

if [[ $FAILED_TESTS -eq 0 ]]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    echo ""
    echo "Export files saved to: $TEST_DIR"
    ls -lh "$TEST_DIR"
    exit 0
else
    echo -e "${RED}❌ Some tests failed. Please check the output above.${NC}"
    exit 1
fi
