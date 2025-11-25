<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
    <!-- Navigation -->
    <nav class="border-b border-slate-700 bg-slate-800/50 backdrop-blur-md sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-3 sm:px-4 md:px-6 lg:px-8">
        <div class="flex items-center justify-between h-14 md:h-16">
          <div class="flex items-center gap-2 md:gap-3 min-w-0">
            <div class="text-xl md:text-2xl flex-shrink-0">🛡️</div>
            <div class="min-w-0">
              <h1 class="text-lg md:text-2xl font-bold text-white truncate">VAMS</h1>
              <p class="text-xs text-slate-400 hidden sm:block">Email Security</p>
            </div>
          </div>
          <div class="text-xs md:text-sm text-slate-400">
            <span v-if="!result">Ready to analyze</span>
            <span v-else class="text-green-400">✓ Complete</span>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-3 sm:px-4 md:px-6 lg:px-8 py-6 md:py-12">
      <!-- Upload Section -->
      <div v-if="!result" class="space-y-6 md:space-y-8">
        <!-- Hero Section -->
        <div class="text-center mb-8 md:mb-12">
          <h2 class="text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-2 md:mb-4">
            Detect Phishing & Spam
          </h2>
          <p class="text-sm md:text-base lg:text-lg text-slate-300 max-w-2xl mx-auto px-2">
            Advanced multi-layer analysis to protect your law firm from malicious emails
          </p>
        </div>

        <!-- Upload Card -->
        <div class="bg-slate-800 border border-slate-700 rounded-xl md:rounded-2xl shadow-2xl p-4 md:p-8 hover:border-slate-600 transition-colors">
          <Upload @analyze="handleAnalyze" />
          <Transition name="fade">
            <div v-if="error" class="mt-4 md:mt-6 p-3 md:p-4 bg-red-900/20 border border-red-500/50 rounded-lg text-red-400 flex items-start gap-2 md:gap-3">
              <span class="text-lg md:text-xl flex-shrink-0">⚠️</span>
              <div class="min-w-0">
                <p class="font-semibold text-sm md:text-base">Analysis Error</p>
                <p class="text-xs md:text-sm mt-1 break-words">{{ error }}</p>
              </div>
            </div>
          </Transition>
        </div>

        <!-- Info Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3 md:gap-6 mt-8 md:mt-12">
          <div class="bg-slate-800 border border-slate-700 rounded-lg md:rounded-xl p-4 md:p-6 hover:border-blue-500/50 transition-colors">
            <div class="text-2xl md:text-3xl mb-2 md:mb-3">🔍</div>
            <h3 class="font-semibold text-white text-sm md:text-base mb-1 md:mb-2">Multi-Layer Detection</h3>
            <p class="text-xs md:text-sm text-slate-300">Analyzes headers, URLs, content, and attachments</p>
          </div>
          <div class="bg-slate-800 border border-slate-700 rounded-lg md:rounded-xl p-4 md:p-6 hover:border-purple-500/50 transition-colors">
            <div class="text-2xl md:text-3xl mb-2 md:mb-3">⚡</div>
            <h3 class="font-semibold text-white text-sm md:text-base mb-1 md:mb-2">Real-Time Analysis</h3>
            <p class="text-xs md:text-sm text-slate-300">Instant results without storing data</p>
          </div>
          <div class="bg-slate-800 border border-slate-700 rounded-lg md:rounded-xl p-4 md:p-6 hover:border-green-500/50 transition-colors">
            <div class="text-2xl md:text-3xl mb-2 md:mb-3">🔒</div>
            <h3 class="font-semibold text-white text-sm md:text-base mb-1 md:mb-2">Privacy First</h3>
            <p class="text-xs md:text-sm text-slate-300">Emails never persisted to disk</p>
          </div>
        </div>
      </div>

      <!-- Results Section -->
      <Transition name="slide-fade">
        <div v-if="result" class="space-y-4 md:space-y-6">
          <!-- Back Button -->
          <button 
            @click="reset"
            class="inline-flex items-center gap-2 px-3 md:px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition-colors border border-slate-700 hover:border-slate-600 text-sm md:text-base"
          >
            ← Back
          </button>

          <!-- Risk Banner -->
          <RiskBanner 
            :score="result.phishing.score"
            :spam-score="result.spam.score"
            :classification="result.classification"
            :recommendation="result.recommendation"
            :metadata="result.metadata"
          />

          <!-- Dashboard -->
          <Dashboard 
            :metadata="result.metadata"
            :phishing="result.phishing"
            :spam="result.spam"
            :classification="result.classification"
          />
        </div>
      </Transition>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Upload from './components/Upload.vue'
import RiskBanner from './components/RiskBanner.vue'
import Dashboard from './components/Dashboard.vue'

const result = ref(null)
const error = ref(null)

const handleAnalyze = async (formData) => {
  error.value = null
  try {
    const response = await fetch('http://localhost:8000/api/analyze', {
      method: 'POST',
      body: formData
    })
    
    if (!response.ok) {
      throw new Error('Analysis failed')
    }
    
    result.value = await response.json()
  } catch (e) {
    error.value = "Failed to analyze email. Is the backend running?"
    console.error(e)
  }
}

const reset = () => {
  result.value = null
  error.value = null
}

</script>
