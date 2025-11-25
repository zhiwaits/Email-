<template>
  <div class="space-y-6">
    <!-- Tab Navigation -->
    <div class="flex gap-2 border-b border-slate-700">
      <button
        @click="activeTab = 'file'"
        class="px-4 py-3 font-medium text-sm transition-colors border-b-2"
        :class="activeTab === 'file' 
          ? 'border-blue-500 text-blue-400' 
          : 'border-transparent text-slate-400 hover:text-slate-300'"
      >
        📁 Upload .eml File
      </button>
      <button
        @click="activeTab = 'paste'"
        class="px-4 py-3 font-medium text-sm transition-colors border-b-2"
        :class="activeTab === 'paste' 
          ? 'border-blue-500 text-blue-400' 
          : 'border-transparent text-slate-400 hover:text-slate-300'"
      >
        📋 Paste Email Content
      </button>
      <button
        @click="activeTab = 'sample'"
        class="px-4 py-3 font-medium text-sm transition-colors border-b-2"
        :class="activeTab === 'sample' 
          ? 'border-blue-500 text-blue-400' 
          : 'border-transparent text-slate-400 hover:text-slate-300'"
      >
        🧪 Sample Phishing
      </button>
    </div>

    <!-- File Upload Tab -->
    <Transition name="fade" mode="out-in">
      <div v-if="activeTab === 'file'" class="space-y-6">
        <div 
          class="relative border-2 border-dashed border-slate-600 rounded-xl p-8 md:p-12 text-center hover:border-blue-500 hover:bg-blue-500/5 transition-all cursor-pointer group"
          @dragover.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false"
          @drop.prevent="handleDrop"
          @click="triggerFileInput"
          :class="{ 'border-blue-500 bg-blue-500/5': isDragging }"
        >
          <input 
            type="file" 
            ref="fileInput" 
            class="hidden" 
            accept=".eml" 
            @change="handleFileSelect"
          >

          <!-- Icon Animation -->
          <div class="mb-4 text-6xl md:text-8xl transition-transform group-hover:scale-110" :class="selectedFile ? '📄' : '📧'"></div>

          <!-- Content -->
          <div v-if="!selectedFile" class="space-y-2">
            <h3 class="text-lg md:text-xl font-semibold text-white">Drop your email file here</h3>
            <p class="text-sm text-slate-400">or click to browse (.eml files only)</p>
            <p class="text-xs text-slate-500 mt-3">Max file size: 50MB</p>
          </div>

          <div v-else class="space-y-4">
            <div class="break-all md:break-normal">
              <h3 class="text-lg md:text-xl font-semibold text-white truncate">{{ selectedFile.name }}</h3>
              <p class="text-sm text-slate-400 mt-1">{{ formatFileSize(selectedFile.size) }}</p>
            </div>
            <div class="flex flex-col sm:flex-row gap-2 justify-center">
              <button 
                @click.stop="analyzeFile"
                class="px-6 py-2 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-medium rounded-lg transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                :disabled="loading"
              >
                <span v-if="!loading">✓ Analyze Email</span>
                <span v-else class="flex items-center gap-2">
                  <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Analyzing...
                </span>
              </button>
              <button 
                @click.stop="selectedFile = null"
                class="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-slate-200 font-medium rounded-lg transition-colors"
              >
                Change
              </button>
            </div>
          </div>
        </div>

        <!-- Progress Bar -->
        <Transition name="fade">
          <div v-if="loading" class="bg-slate-700/50 rounded-lg p-4">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-medium text-white">Analyzing email security...</span>
              <span class="text-xs text-slate-400">{{ progress }}%</span>
            </div>
            <div class="w-full bg-slate-600 rounded-full h-2 overflow-hidden">
              <div 
                class="bg-gradient-to-r from-blue-500 to-purple-500 h-full rounded-full transition-all duration-300"
                :style="{ width: progress + '%' }"
              ></div>
            </div>
          </div>
        </Transition>
      </div>

      <!-- Paste Email Tab -->
      <div v-else-if="activeTab === 'paste'" class="space-y-6">
        <div class="space-y-4">
          <textarea
            v-model="emailContent"
            placeholder="Paste your complete email here (including headers)&#10;&#10;Example:&#10;From: sender@example.com&#10;To: recipient@lawfirm.com&#10;Subject: Important Document&#10;&#10;Email body content..."
            class="w-full h-64 md:h-96 p-4 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 font-mono text-sm resize-none"
          ></textarea>
          
          <div class="flex flex-col sm:flex-row gap-2">
            <button
              @click="analyzeContent"
              class="px-6 py-2 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-medium rounded-lg transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              :disabled="!emailContent.trim() || loading"
            >
              <span v-if="!loading">✓ Analyze</span>
              <span v-else class="flex items-center gap-2">
                <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Analyzing...
              </span>
            </button>
            <button
              @click="emailContent = ''"
              class="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-slate-200 font-medium rounded-lg transition-colors"
            >
              Clear
            </button>
          </div>
        </div>

        <!-- Progress Bar -->
        <Transition name="fade">
          <div v-if="loading" class="bg-slate-700/50 rounded-lg p-4">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-medium text-white">Analyzing email security...</span>
              <span class="text-xs text-slate-400">{{ progress }}%</span>
            </div>
            <div class="w-full bg-slate-600 rounded-full h-2 overflow-hidden">
              <div 
                class="bg-gradient-to-r from-blue-500 to-purple-500 h-full rounded-full transition-all duration-300"
                :style="{ width: progress + '%' }"
              ></div>
            </div>
          </div>
        </Transition>
      </div>

      <!-- Sample Phishing Tab -->
      <div v-else-if="activeTab === 'sample'" class="space-y-6">
        <div class="bg-slate-700/50 border border-slate-600 rounded-lg p-6">
          <h3 class="text-lg font-semibold text-white mb-3">📧 Sample Phishing Email</h3>
          <p class="text-sm text-slate-300 mb-4">This is a realistic phishing example. Click analyze to see how VAMS detects it.</p>
          <pre class="bg-slate-800 p-4 rounded-lg overflow-x-auto text-xs text-slate-300 mb-4 max-h-64 overflow-y-auto font-mono">{{ samplePhishingEmail }}</pre>
          <button
            @click="analyzeSample"
            class="w-full px-6 py-2 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-medium rounded-lg transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            :disabled="loading"
          >
            <span v-if="!loading">🧪 Analyze Sample</span>
            <span v-else class="flex items-center gap-2">
              <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Analyzing...
            </span>
          </button>
        </div>

        <!-- Progress Bar -->
        <Transition name="fade">
          <div v-if="loading" class="bg-slate-700/50 rounded-lg p-4">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-medium text-white">Analyzing email security...</span>
              <span class="text-xs text-slate-400">{{ progress }}%</span>
            </div>
            <div class="w-full bg-slate-600 rounded-full h-2 overflow-hidden">
              <div 
                class="bg-gradient-to-r from-blue-500 to-purple-500 h-full rounded-full transition-all duration-300"
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
