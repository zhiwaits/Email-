<template>
  <div class="w-full space-y-6 md:space-y-8 lg:space-y-10">
    <!-- Tab Navigation -->
    <div class="w-full flex gap-1 md:gap-2 border-b border-slate-700/50 backdrop-blur-xl overflow-x-auto">
      <button
        @click="activeTab = 'file'"
        class="px-4 md:px-6 py-3 md:py-4 font-bold text-sm md:text-base transition-all duration-300 border-b-3 relative group"
        :class="activeTab === 'file' 
          ? 'border-green-500 text-green-400 bg-green-500/5' 
          : 'border-transparent text-slate-400 hover:text-slate-300 hover:bg-slate-700/30'"
      >
        📁 Upload .eml File
        <span v-if="activeTab === 'file'" class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full"></span>
      </button>
      <button
        @click="activeTab = 'paste'"
        class="px-4 md:px-6 py-3 md:py-4 font-bold text-sm md:text-base transition-all duration-300 border-b-3 relative group"
        :class="activeTab === 'paste' 
          ? 'border-green-500 text-green-400 bg-green-500/5' 
          : 'border-transparent text-slate-400 hover:text-slate-300 hover:bg-slate-700/30'"
      >
        📋 Paste Email Content
        <span v-if="activeTab === 'paste'" class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full"></span>
      </button>
      <button
        @click="activeTab = 'sample'"
        class="px-4 md:px-6 py-3 md:py-4 font-bold text-sm md:text-base transition-all duration-300 border-b-3 relative group"
        :class="activeTab === 'sample' 
          ? 'border-green-500 text-green-400 bg-green-500/5' 
          : 'border-transparent text-slate-400 hover:text-slate-300 hover:bg-slate-700/30'"
      >
        🧪 Sample Phishing
        <span v-if="activeTab === 'sample'" class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full"></span>
      </button>
    </div>

    <!-- File Upload Tab -->
    <Transition name="fade" mode="out-in">
      <div v-if="activeTab === 'file'" class="space-y-6 md:space-y-8 animate-fade-in">
        <div 
          class="relative border-3 border-dashed border-slate-600 rounded-2xl p-12 md:p-20 lg:p-24 text-center hover:border-green-500 hover:bg-gradient-to-br hover:from-green-500/10 hover:to-emerald-500/10 transition-all duration-300 cursor-pointer group overflow-hidden backdrop-blur-xl"
          @dragover.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false"
          @drop.prevent="handleDrop"
          @click="triggerFileInput"
          :class="{ 'border-green-500 bg-gradient-to-br from-green-500/20 to-emerald-500/20 shadow-2xl shadow-green-500/20': isDragging }"
        >
          <div class="absolute inset-0 bg-gradient-to-r from-blue-500/0 to-purple-500/0 group-hover:from-blue-500/5 group-hover:to-purple-500/5 transition-all duration-300 pointer-events-none"></div>
          
          <input 
            type="file" 
            ref="fileInput" 
            class="hidden" 
            accept=".eml" 
            @change="handleFileSelect"
          >

          <!-- Icon Animation -->
          <div class="mb-6 text-8xl md:text-9xl transition-all duration-300 group-hover:scale-125 group-hover:animate-pulse" :class="selectedFile ? '' : ''" style="animation-delay: 0s;">{{ selectedFile ? '📄' : '📧' }}</div>

          <!-- Content -->
          <div v-if="!selectedFile" class="space-y-3 relative">
            <h3 class="text-2xl md:text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">Drop your email file here</h3>
            <p class="text-base md:text-lg text-slate-300">or click to browse (.eml files only)</p>
            <p class="text-xs md:text-sm text-slate-500 mt-4">📦 Max file size: 50MB</p>
          </div>

          <div v-else class="space-y-5 relative">
            <div class="break-all md:break-normal bg-slate-700/50 backdrop-blur rounded-xl p-4">
              <h3 class="text-xl md:text-2xl font-bold text-white truncate">{{ selectedFile.name }}</h3>
              <p class="text-sm text-slate-400 mt-2">{{ formatFileSize(selectedFile.size) }}</p>
            </div>
            <div class="flex flex-col sm:flex-row gap-3 justify-center">
              <button 
                @click.stop="analyzeFile"
                class="px-6 md:px-8 py-3 md:py-4 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white font-bold rounded-xl transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-lg hover:shadow-green-500/30 text-sm md:text-base"
                :disabled="loading"
              >
                <span v-if="!loading">✓ Analyze Email</span>
                <span v-else class="flex items-center gap-2">
                  <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Analyzing...
                </span>
              </button>
              <button 
                @click.stop="selectedFile = null"
                class="px-6 md:px-8 py-3 md:py-4 bg-gradient-to-r from-slate-700 to-slate-800 hover:from-slate-600 hover:to-slate-700 text-slate-200 font-bold rounded-xl transition-all shadow-lg text-sm md:text-base"
              >
                Change
              </button>
            </div>
          </div>
        </div>

        <!-- Progress Bar -->
        <Transition name="fade">
          <div v-if="loading" class="bg-gradient-to-r from-slate-700/50 to-slate-800/50 backdrop-blur border border-slate-600/30 rounded-2xl p-5 md:p-6 shadow-lg">
            <div class="flex items-center justify-between mb-3">
              <span class="text-sm md:text-base font-bold text-white">Analyzing email security...</span>
              <span class="text-xs md:text-sm text-slate-300 font-bold">{{ progress }}%</span>
            </div>
            <div class="w-full bg-slate-600/50 rounded-full h-3 overflow-hidden backdrop-blur">
              <div 
                class="bg-gradient-to-r from-green-500 via-emerald-500 to-green-600 h-full rounded-full transition-all duration-300 shadow-lg shadow-green-500/50"
                :style="{ width: progress + '%' }"
              ></div>
            </div>
          </div>
        </Transition>
      </div>

      <!-- Paste Email Tab -->
      <div v-else-if="activeTab === 'paste'" class="space-y-6 md:space-y-8 animate-fade-in">
        <div class="space-y-4">
          <textarea
            v-model="emailContent"
            placeholder="Paste your complete email here (including headers)&#10;&#10;Example:&#10;From: sender@example.com&#10;To: recipient@lawfirm.com&#10;Subject: Important Document&#10;&#10;Email body content..."
            class="w-full h-64 md:h-96 p-5 md:p-6 bg-gradient-to-br from-slate-700 to-slate-800 border-2 border-slate-600 hover:border-green-500/50 rounded-2xl text-white placeholder-slate-500 focus:outline-none focus:border-green-500 focus:ring-2 focus:ring-green-500/30 font-mono text-sm resize-none transition-all duration-300 backdrop-blur"
          ></textarea>
          
          <div class="flex flex-col sm:flex-row gap-3">
            <button
              @click="analyzeContent"
              class="px-6 md:px-8 py-3 md:py-4 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white font-bold rounded-xl transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-lg hover:shadow-green-500/30 text-sm md:text-base flex-1"
              :disabled="!emailContent.trim() || loading"
            >
              <span v-if="!loading">✓ Analyze</span>
              <span v-else class="flex items-center gap-2">
                <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Analyzing...
              </span>
            </button>
            <button
              @click="emailContent = ''"
              class="px-6 md:px-8 py-3 md:py-4 bg-gradient-to-r from-slate-700 to-slate-800 hover:from-slate-600 hover:to-slate-700 text-slate-200 font-bold rounded-xl transition-all shadow-lg text-sm md:text-base"
            >
              Clear
            </button>
          </div>
        </div>

        <!-- Progress Bar -->
        <Transition name="fade">
          <div v-if="loading" class="bg-gradient-to-r from-slate-700/50 to-slate-800/50 backdrop-blur border border-slate-600/30 rounded-2xl p-5 md:p-6 shadow-lg">
            <div class="flex items-center justify-between mb-3">
              <span class="text-sm md:text-base font-bold text-white">Analyzing email security...</span>
              <span class="text-xs md:text-sm text-slate-300 font-bold">{{ progress }}%</span>
            </div>
            <div class="w-full bg-slate-600/50 rounded-full h-3 overflow-hidden backdrop-blur">
              <div 
                class="bg-gradient-to-r from-green-500 via-emerald-500 to-green-600 h-full rounded-full transition-all duration-300 shadow-lg shadow-green-500/50"
                :style="{ width: progress + '%' }"
              ></div>
            </div>
          </div>
        </Transition>
      </div>

      <!-- Sample Phishing Tab -->
      <div v-else-if="activeTab === 'sample'" class="w-full space-y-6 md:space-y-8 lg:space-y-10 animate-fade-in">
        <div class="w-full group relative overflow-hidden bg-gradient-to-br from-slate-800 to-slate-900 border-2 border-slate-700/50 rounded-2xl md:rounded-3xl p-8 md:p-10 lg:p-12 hover:border-pink-500/30 transition-all duration-300">
          <div class="absolute inset-0 bg-gradient-to-r from-pink-500/0 to-pink-500/0 group-hover:from-pink-500/5 group-hover:to-red-500/5 transition-all duration-300 pointer-events-none"></div>
          <div class="relative">
            <div class="mb-5 md:mb-6">
              <h3 class="text-xl md:text-2xl font-bold text-white mb-2">📧 Sample Phishing Email</h3>
              <p class="text-sm md:text-base text-slate-300">This is a realistic phishing example. Click analyze to see how VAMS detects it.</p>
            </div>
            <pre class="bg-slate-800/70 border border-slate-700/50 p-4 md:p-6 rounded-xl overflow-x-auto text-xs md:text-sm text-slate-300 mb-6 md:mb-8 max-h-96 overflow-y-auto font-mono backdrop-blur w-full">{{ samplePhishingEmail }}</pre>
            <button
              @click="analyzeSample"
              class="w-full px-6 md:px-8 py-4 md:py-5 lg:py-6 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white font-bold rounded-xl transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-lg hover:shadow-green-500/30 text-sm md:text-base lg:text-lg"
              :disabled="loading"
            >
              <span v-if="!loading">🧪 Analyze Sample</span>
              <span v-else class="flex items-center gap-2">
                <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Analyzing...
              </span>
            </button>
          </div>
        </div>

        <!-- Progress Bar -->
        <Transition name="fade">
          <div v-if="loading" class="bg-gradient-to-r from-slate-700/50 to-slate-800/50 backdrop-blur border border-slate-600/30 rounded-2xl p-5 md:p-6 shadow-lg">
            <div class="flex items-center justify-between mb-3">
              <span class="text-sm md:text-base font-bold text-white">Analyzing email security...</span>
              <span class="text-xs md:text-sm text-slate-300 font-bold">{{ progress }}%</span>
            </div>
            <div class="w-full bg-slate-600/50 rounded-full h-3 overflow-hidden backdrop-blur">
              <div 
                class="bg-gradient-to-r from-green-500 via-emerald-500 to-green-600 h-full rounded-full transition-all duration-300 shadow-lg shadow-green-500/50"
                :style="{ width: progress + '%' }"
              ></div>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['analyze'])
const fileInput = ref(null)
const selectedFile = ref(null)
const loading = ref(false)
const isDragging = ref(false)
const progress = ref(0)
const activeTab = ref('file')
const emailContent = ref('')

const samplePhishingEmail = `From: CEO <ceo@lawfirm-usa.com>
To: accounting@lawfirm.com
Subject: URGENT: Wire Transfer Required Today
Date: Mon, 24 Nov 2025 14:30:00 +0000

Dear Finance Team,

URGENT ACTION REQUIRED!

We need to immediately process a wire transfer of $250,000 USD for a client settlement. Due to confidentiality, this must be handled discreetly.

Please wire funds to:
Bank: First International Bank
Account: 987654321
Routing: 123456789

This is time-sensitive - please confirm transfer within 1 hour.

CEO`

const triggerFileInput = () => {
  fileInput.value.click()
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) processFile(file)
}

const handleDrop = (event) => {
  isDragging.value = false
  const file = event.dataTransfer.files[0]
  if (file) processFile(file)
}

const processFile = (file) => {
  if (!file.name.endsWith('.eml')) {
    alert('Please upload a .eml file')
    return
  }
  if (file.size > 50 * 1024 * 1024) {
    alert('File too large (max 50MB)')
    return
  }
  selectedFile.value = file
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

const startProgress = () => {
  loading.value = true
  progress.value = 0
  const progressInterval = setInterval(() => {
    progress.value = Math.min(progress.value + Math.random() * 30, 90)
  }, 200)
  return progressInterval
}

const endProgress = (progressInterval) => {
  setTimeout(() => {
    clearInterval(progressInterval)
    loading.value = false
    progress.value = 0
  }, 500)
}

const analyzeFile = async () => {
  if (!selectedFile.value) return
  
  const progressInterval = startProgress()

  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    
    emit('analyze', formData)
    progress.value = 100
  } catch (error) {
    console.error(error)
  } finally {
    endProgress(progressInterval)
  }
}

const analyzeContent = async () => {
  if (!emailContent.value.trim()) return
  
  const progressInterval = startProgress()

  try {
    // Convert email content to a Blob and create FormData
    const blob = new Blob([emailContent.value], { type: 'text/plain' })
    const file = new File([blob], 'email.eml', { type: 'message/rfc822' })
    
    const formData = new FormData()
    formData.append('file', file)
    
    emit('analyze', formData)
    progress.value = 100
  } catch (error) {
    console.error(error)
  } finally {
    endProgress(progressInterval)
  }
}

const analyzeSample = async () => {
  const progressInterval = startProgress()

  try {
    const blob = new Blob([samplePhishingEmail], { type: 'text/plain' })
    const file = new File([blob], 'sample_phishing.eml', { type: 'message/rfc822' })
    
    const formData = new FormData()
    formData.append('file', file)
    
    emit('analyze', formData)
    progress.value = 100
  } catch (error) {
    console.error(error)
  } finally {
    endProgress(progressInterval)
  }
}
</script>
