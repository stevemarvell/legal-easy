#!/usr/bin/env node

/**
 * Simple script to test if the backend API is accessible
 */

const API_BASE_URL = 'http://localhost:8000';

async function testAPI() {
  console.log('🔍 Testing backend API connectivity...\n');
  
  try {
    // Test basic connectivity
    console.log('1. Testing basic connectivity...');
    const healthResponse = await fetch(`${API_BASE_URL}/`);
    console.log(`   Status: ${healthResponse.status}`);
    
    if (healthResponse.ok) {
      console.log('   ✅ Backend is accessible');
    } else {
      console.log('   ❌ Backend returned error status');
    }
    
    // Test cases endpoint
    console.log('\n2. Testing cases endpoint...');
    const casesResponse = await fetch(`${API_BASE_URL}/api/cases`);
    console.log(`   Status: ${casesResponse.status}`);
    
    if (casesResponse.ok) {
      const casesData = await casesResponse.json();
      console.log(`   ✅ Cases endpoint working - ${casesData.length} cases found`);
      
      if (casesData.length > 0) {
        const firstCase = casesData[0];
        console.log(`   First case ID: ${firstCase.id}`);
        
        // Test specific case endpoint
        console.log('\n3. Testing specific case endpoint...');
        const caseResponse = await fetch(`${API_BASE_URL}/api/cases/${firstCase.id}`);
        console.log(`   Status: ${caseResponse.status}`);
        
        if (caseResponse.ok) {
          const caseData = await caseResponse.json();
          console.log(`   ✅ Case detail endpoint working - Case: ${caseData.title}`);
        } else {
          console.log('   ❌ Case detail endpoint failed');
        }
      }
    } else {
      console.log('   ❌ Cases endpoint failed');
      const errorText = await casesResponse.text();
      console.log(`   Error: ${errorText}`);
    }
    
  } catch (error) {
    console.log('❌ Failed to connect to backend API');
    console.log(`Error: ${error.message}`);
    console.log('\n💡 Make sure the backend server is running on http://localhost:8000');
    console.log('   You can start it with: cd backend && python main.py');
  }
}

testAPI();