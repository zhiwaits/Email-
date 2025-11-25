<template>
  <div class="min-h-screen bg-gradient-to-br from-black via-slate-900 to-black">
    <!-- Animated Background Elements -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-0 left-1/4 w-96 h-96 bg-green-500/10 rounded-full blur-3xl animate-float"></div>
      <div class="absolute bottom-0 right-1/4 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl animate-float" style="animation-delay: 1s;"></div>
    </div>

    <!-- Navigation -->
      <nav class="border-b border-slate-700/50 bg-gradient-to-r from-black/80 via-slate-900/80 to-black/80 backdrop-blur-xl sticky top-0 z-50 w-screen overflow-x-hidden">
      <div class="w-full pl-2 sm:pl-3 md:pl-4 lg:pl-6 xl:pl-8 pr-6 sm:pr-8 md:pr-10 lg:pr-12">
        <div class="flex items-center justify-between h-16 md:h-20 min-w-0">
          <div class="flex items-center gap-2 md:gap-3 flex-shrink-0">
            <div class="text-xl md:text-2xl">🛡️</div>
            <div class="min-w-0 hidden sm:block">
              <h1 class="text-xl md:text-2xl font-bold bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent truncate">VAMS</h1>
              <p class="text-xs text-slate-400 hidden md:block">Advanced Email Security</p>
            </div>
            <div class="min-w-0 sm:hidden">
              <h1 class="text-xl font-bold bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent">VAMS</h1>
            </div>
          </div>
          <div class="text-xs md:text-sm text-slate-400 flex items-center gap-1.5 flex-shrink-0 ml-auto">
            <span v-if="!result" class="flex items-center gap-1 whitespace-nowrap">
              <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse flex-shrink-0"></div>
              <span class="hidden sm:inline">Ready to analyze</span>
              <span class="inline sm:hidden">Ready</span>
            </span>
            <span v-else class="flex items-center gap-1 text-green-400 whitespace-nowrap">
              <div class="w-2 h-2 bg-green-400 rounded-full flex-shrink-0"></div>
              <span class="hidden sm:inline">✓ Analysis Complete</span>
              <span class="inline sm:hidden">✓ Complete</span>
            </span>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="relative w-screen py-12 md:py-20 lg:py-24 z-10 px-2 sm:px-3 md:px-4 lg:px-6 xl:px-8 2xl:px-10">
      <!-- Upload Section -->
      <div v-if="!result" class="space-y-12 md:space-y-16 lg:space-y-20">
        <!-- Hero Section -->
        <div class="text-center mb-16 md:mb-20 lg:mb-24 space-y-6 md:space-y-8 lg:space-y-10">
          <div class="inline-block">
            <span class="px-4 py-2 rounded-full text-xs md:text-sm font-semibold text-green-400 bg-green-500/10 border border-green-500/30">
              🔐 Enterprise Email Security
            </span>
          </div>
          <h2 class="text-3xl md:text-5xl lg:text-7xl font-bold text-white leading-tight w-full break-words">
            Advanced <span class="bg-gradient-to-r from-green-400 via-green-500 to-emerald-400 bg-clip-text text-transparent">Phishing Detection</span>
          </h2>
          <p class="text-base md:text-lg text-slate-300 px-4 leading-relaxed">
            Multi-layer intelligence to protect your law firm from sophisticated email attacks, credential theft, and social engineering
          </p>
        </div>

        <!-- Upload Card -->
        <div class="w-full card border-2 border-slate-700/50 hover:border-green-500/30 hover:shadow-xl hover:shadow-green-500/10">
          <Upload @analyze="handleAnalyze" />
          <Transition name="fade">
            <div v-if="error" class="mt-6 md:mt-8 p-4 md:p-6 bg-red-900/20 border border-red-500/50 rounded-xl text-red-400 flex items-start gap-3 md:gap-4 backdrop-blur">
              <span class="text-2xl md:text-3xl flex-shrink-0">⚠️</span>
              <div class="min-w-0">
                <p class="font-semibold text-sm md:text-base">Analysis Error</p>
                <p class="text-xs md:text-sm mt-2 break-words text-red-300">{{ error }}</p>
              </div>
            </div>
          </Transition>
        </div>

        <!-- Info Cards -->
        <div class="w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8 lg:gap-10 mt-16 md:mt-20 lg:mt-24">
          <!-- Multi-Layer Detection -->
          <div class="group relative overflow-hidden">
            <div class="absolute inset-0 bg-gradient-to-r from-green-500/0 to-green-500/0 group-hover:from-green-500/10 group-hover:to-emerald-500/10 transition-all duration-300 rounded-2xl"></div>
            <div class="card h-full relative border-green-500/20 group-hover:border-green-500/50">
              <div class="text-6xl md:text-7xl mb-5 md:mb-6">🔍</div>
              <h3 class="font-bold text-white text-xl md:text-2xl lg:text-3xl mb-3 md:mb-4">Multi-Layer Detection</h3>
              <p class="text-base md:text-lg lg:text-xl text-slate-300 leading-relaxed">Analyzes headers, URLs, content, attachments, and behavioral patterns</p>
              <div class="mt-4 pt-4 border-t border-slate-700/50">
                <span class="text-sm md:text-base font-semibold text-green-400">125+ Detection Indicators</span>
              </div>
            </div>
          </div>

          <!-- Real-Time Analysis -->
          <div class="group relative overflow-hidden">
            <div class="absolute inset-0 bg-gradient-to-r from-green-500/0 to-green-500/0 group-hover:from-green-500/10 group-hover:to-emerald-500/10 transition-all duration-300 rounded-2xl"></div>
            <div class="card h-full relative border-green-500/20 group-hover:border-green-500/50">
              <div class="text-6xl md:text-7xl mb-5 md:mb-6">⚡</div>
              <h3 class="font-bold text-white text-xl md:text-2xl lg:text-3xl mb-3 md:mb-4">Instant Analysis</h3>
              <p class="text-base md:text-lg lg:text-xl text-slate-300 leading-relaxed">Get results in milliseconds without storing emails or data</p>
              <div class="mt-4 pt-4 border-t border-slate-700/50">
                <span class="text-sm md:text-base font-semibold text-green-400">&lt; 1 Second Response</span>
              </div>
            </div>
          </div>

          <!-- Privacy First -->
          <div class="group relative overflow-hidden">
            <div class="absolute inset-0 bg-gradient-to-r from-emerald-500/0 to-emerald-500/0 group-hover:from-emerald-500/10 group-hover:to-green-500/10 transition-all duration-300 rounded-2xl"></div>
            <div class="card h-full relative border-emerald-500/20 group-hover:border-emerald-500/50">
              <div class="text-6xl md:text-7xl mb-5 md:mb-6">🔒</div>
              <h3 class="font-bold text-white text-xl md:text-2xl lg:text-3xl mb-3 md:mb-4">Privacy First</h3>
              <p class="text-base md:text-lg lg:text-xl text-slate-300 leading-relaxed">Zero disk persistence, memory-only processing, no data retention</p>
              <div class="mt-4 pt-4 border-t border-slate-700/50">
                <span class="text-sm md:text-base font-semibold text-emerald-400">Fully Compliant</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Results Section -->
      <Transition name="slide-fade">
        <div v-if="result" class="space-y-8 md:space-y-12 lg:space-y-16 py-8 md:py-12 lg:py-16">
          <!-- Back Button -->
          <button 
            @click="reset"
            class="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-slate-800/50 hover:bg-slate-700/50 text-slate-300 hover:text-white transition-all border border-slate-700/50 hover:border-slate-600/50 text-sm md:text-base font-medium hover:shadow-lg"
          >
            ← Back to Upload
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
