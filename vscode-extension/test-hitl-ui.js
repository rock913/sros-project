/**
 * HITL UI Test Script
 * 
 * This script tests the HITL UI generation functions
 */

const fs = require('fs');
const path = require('path');

// Load the compiled HITL module
const hitlModule = require('./out/hitlWebview');

console.log('='.repeat(60));
console.log('HITL UI Test Script');
console.log('='.repeat(60));

// Test 1: Query Approval Card
console.log('\n✅ Test 1: Query Approval Card');
const queryRequest = {
    request_id: 'hitl_query_test123',
    decision_type: 'query_approval',
    prompt: 'Please approve the following queries',
    options: ['approve', 'reject', 'modify'],
    context: {
        research_topic: 'Quantum Computing Applications',
        queries: [
            'quantum computing applications in cryptography',
            'recent advances in quantum algorithms',
            'quantum computing hardware developments'
        ]
    },
    timeout_seconds: 300
};

try {
    const queryHTML = hitlModule.generateHITLDecisionCardHTML(queryRequest);
    console.log(`   Generated HTML length: ${queryHTML.length} characters`);
    
    // Save to file for inspection
    const queryOutputPath = path.join(__dirname, 'test-output-query.html');
    fs.writeFileSync(queryOutputPath, queryHTML);
    console.log(`   Saved to: ${queryOutputPath}`);
    
    // Basic validation
    if (queryHTML.includes('Query Approval') && 
        queryHTML.includes('quantum computing') &&
        queryHTML.includes('approve') &&
        queryHTML.includes('reject')) {
        console.log('   ✅ Query Approval Card: PASSED');
    } else {
        console.log('   ❌ Query Approval Card: FAILED - Missing expected content');
    }
} catch (error) {
    console.log(`   ❌ Query Approval Card: FAILED - ${error.message}`);
}

// Test 2: Paper Selection Card
console.log('\n✅ Test 2: Paper Selection Card');
const paperRequest = {
    request_id: 'hitl_paper_test456',
    decision_type: 'paper_selection',
    prompt: 'Select papers to analyze',
    options: ['select_all', 'select_subset', 'reject'],
    context: {
        total_count: 35,
        papers: [
            {
                title: 'Quantum Error Correction Codes',
                authors: ['John Doe', 'Jane Smith'],
                year: 2023,
                doi: '10.1234/quantum.2023.001',
                abstract: 'This paper presents novel quantum error correction codes...'
            },
            {
                title: 'Superconducting Quantum Processors',
                authors: ['Alice Johnson'],
                year: 2024,
                doi: '10.1234/quantum.2024.002',
                abstract: 'Recent advances in superconducting quantum processors...'
            }
        ]
    },
    timeout_seconds: 600
};

try {
    const paperHTML = hitlModule.generateHITLDecisionCardHTML(paperRequest);
    console.log(`   Generated HTML length: ${paperHTML.length} characters`);
    
    // Save to file for inspection
    const paperOutputPath = path.join(__dirname, 'test-output-paper.html');
    fs.writeFileSync(paperOutputPath, paperHTML);
    console.log(`   Saved to: ${paperOutputPath}`);
    
    // Basic validation
    if (paperHTML.includes('Paper Selection') && 
        paperHTML.includes('35') &&
        paperHTML.includes('Quantum Error Correction') &&
        paperHTML.includes('select_all')) {
        console.log('   ✅ Paper Selection Card: PASSED');
    } else {
        console.log('   ❌ Paper Selection Card: FAILED - Missing expected content');
    }
} catch (error) {
    console.log(`   ❌ Paper Selection Card: FAILED - ${error.message}`);
}

// Test 3: Report Revision Card
console.log('\n✅ Test 3: Report Revision Card');
const reportRequest = {
    request_id: 'hitl_report_test789',
    decision_type: 'report_revision',
    prompt: 'Review the research report',
    options: ['approve', 'modify', 'reject'],
    context: {
        research_topic: 'Quantum Computing Applications',
        report: `# Quantum Computing Applications

## Introduction
Quantum computing represents a paradigm shift in computational power...

## Recent Advances
Recent developments in quantum error correction have enabled...

## Conclusion
The field of quantum computing continues to evolve rapidly...`,
        word_count: 250,
        paper_count: 15
    },
    timeout_seconds: 900
};

try {
    const reportHTML = hitlModule.generateHITLDecisionCardHTML(reportRequest);
    console.log(`   Generated HTML length: ${reportHTML.length} characters`);
    
    // Save to file for inspection
    const reportOutputPath = path.join(__dirname, 'test-output-report.html');
    fs.writeFileSync(reportOutputPath, reportHTML);
    console.log(`   Saved to: ${reportOutputPath}`);
    
    // Basic validation
    if (reportHTML.includes('Report Revision') && 
        reportHTML.includes('250') &&
        reportHTML.includes('Quantum Computing') &&
        reportHTML.includes('approve')) {
        console.log('   ✅ Report Revision Card: PASSED');
    } else {
        console.log('   ❌ Report Revision Card: FAILED - Missing expected content');
    }
} catch (error) {
    console.log(`   ❌ Report Revision Card: FAILED - ${error.message}`);
}

// Test 4: Invalid decision type
console.log('\n✅ Test 4: Invalid Decision Type');
const invalidRequest = {
    request_id: 'hitl_invalid_test',
    decision_type: 'invalid_type',
    prompt: 'This should fail',
    options: [],
    context: {},
    timeout_seconds: 300
};

try {
    const invalidHTML = hitlModule.generateHITLDecisionCardHTML(invalidRequest);
    if (invalidHTML.includes('Unknown decision type')) {
        console.log('   ✅ Invalid Type Handling: PASSED');
    } else {
        console.log('   ❌ Invalid Type Handling: FAILED - Should show error');
    }
} catch (error) {
    console.log(`   ✅ Invalid Type Handling: PASSED (threw error as expected)`);
}

console.log('\n' + '='.repeat(60));
console.log('✅ All HITL UI tests completed!');
console.log('='.repeat(60));
console.log('\nGenerated HTML files:');
console.log('  - test-output-query.html');
console.log('  - test-output-paper.html');
console.log('  - test-output-report.html');
console.log('\nYou can open these files in a browser to visually inspect the UI.');
console.log('='.repeat(60));
