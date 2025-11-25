<template>
  <div class="space-y-8 md:space-y-12 lg:space-y-16">
    <!-- Email Metadata Card -->
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 md:gap-8 lg:gap-10">
      <div class="group relative overflow-hidden bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700/50 rounded-2xl p-6 md:p-8 hover:border-green-500/50 transition-all duration-300">
        <div class="absolute inset-0 bg-gradient-to-r from-green-500/0 to-green-500/0 group-hover:from-green-500/5 group-hover:to-emerald-500/5 transition-all duration-300"></div>
        <div class="relative">
          <h3 class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-4 md:mb-5">Sender</h3>
          <p class="text-xs md:text-sm text-white truncate font-mono" :title="metadata.sender">{{ metadata.sender }}</p>
        </div>
      </div>
      <div class="group relative overflow-hidden bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700/50 rounded-2xl p-6 md:p-8 hover:border-green-500/50 transition-all duration-300">
        <div class="absolute inset-0 bg-gradient-to-r from-green-500/0 to-green-500/0 group-hover:from-green-500/5 group-hover:to-emerald-500/5 transition-all duration-300"></div>
        <div class="relative">
          <h3 class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-4 md:mb-5">Subject</h3>
          <p class="text-xs md:text-sm text-white truncate" :title="metadata.subject">{{ metadata.subject }}</p>
        </div>
      </div>
      <div class="group relative overflow-hidden bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700/50 rounded-2xl p-6 md:p-8 hover:border-green-500/50 transition-all duration-300">
        <div class="absolute inset-0 bg-gradient-to-r from-green-500/0 to-green-500/0 group-hover:from-green-500/5 group-hover:to-emerald-500/5 transition-all duration-300"></div>
        <div class="relative">
          <h3 class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-4 md:mb-5">Attachments</h3>
          <p class="text-2xl md:text-3xl font-bold text-white">{{ metadata.attachment_count }}</p>
          <p class="text-xs text-slate-400 mt-2">{{ metadata.has_attachments ? 'Present' : 'None' }}</p>
        </div>
      </div>
    </div>

    <!-- Analysis Summary Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-8 lg:gap-10 mt-6 md:mt-8 lg:mt-10">
      <!-- Phishing Analysis -->
      <div class="group relative overflow-hidden bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700/50 rounded-2xl p-6 md:p-8 hover:border-green-500/50 transition-all duration-300">
        <div class="absolute inset-0 bg-gradient-to-r from-green-500/0 to-green-500/0 group-hover:from-green-500/5 group-hover:to-emerald-500/5 transition-all duration-300"></div>
        <div class="relative">
          <div class="flex items-center justify-between mb-6 md:mb-8 gap-3">
            <h3 class="text-lg md:text-xl font-bold text-white">🎣 Phishing Analysis</h3>
            <span 
              class="px-3 md:px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider whitespace-nowrap"
              :class="getPhishingBadgeClass"
            >
              {{ phishing.level }}
            </span>
          </div>
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <span class="text-slate-300 text-sm font-medium">Risk Score</span>
              <span class="text-2xl md:text-3xl font-bold" :class="getPhishingColor">{{ phishing.score }}<span class="text-base text-slate-400">/100</span></span>
            </div>
            <div class="w-full bg-slate-700/50 rounded-full h-3 md:h-4 overflow-hidden backdrop-blur">
              <div 
                class="h-full rounded-full transition-all duration-500"
                :class="score >= 70 ? 'from-red-500 to-red-600' : score >= 50 ? 'from-orange-500 to-orange-600' : score >= 30 ? 'from-yellow-500 to-yellow-600' : 'from-green-500 to-green-600'"
                :style="`width: ${score}%`"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Spam Analysis -->
      <div class="group relative overflow-hidden bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700/50 rounded-2xl p-6 md:p-8 hover:border-green-500/50 transition-all duration-300">
        <div class="absolute inset-0 bg-gradient-to-r from-green-500/0 to-green-500/0 group-hover:from-green-500/5 group-hover:to-emerald-500/5 transition-all duration-300"></div>
        <div class="relative">
          <div class="flex items-center justify-between mb-6 md:mb-8 gap-3">
            <h3 class="text-lg md:text-xl font-bold text-white">📧 Spam Analysis</h3>
            <span 
              class="px-3 md:px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider whitespace-nowrap"
              :class="getSpamBadgeClass"
            >
              {{ spam.level }}
            </span>
          </div>
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <span class="text-slate-300 text-sm font-medium">Spam Score</span>
              <span class="text-2xl md:text-3xl font-bold" :class="getSpamColor">{{ spam.score }}<span class="text-base text-slate-400">/100</span></span>
            </div>
            <div class="w-full bg-slate-700/50 rounded-full h-3 md:h-4 overflow-hidden backdrop-blur">
              <div 
                class="h-full rounded-full transition-all duration-500"
                :class="spamScore >= 80 ? 'from-red-500 to-red-600' : spamScore >= 50 ? 'from-orange-500 to-orange-600' : spamScore >= 30 ? 'from-yellow-500 to-yellow-600' : 'from-green-500 to-green-600'"
                :style="`width: ${spamScore}%`"
              ></div>
            </div>
            <p class="text-xs text-slate-400 font-medium">Probability: <span class="text-slate-200 font-bold">{{ (spam.probability * 100).toFixed(0) }}%</span></p>
          </div>
        </div>
      </div>
    </div>

    <!-- Phishing Findings -->
    <div class="group relative overflow-hidden bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700/50 rounded-2xl p-6 md:p-8 hover:border-green-500/50 transition-all duration-300">
      <div class="absolute inset-0 bg-gradient-to-r from-green-500/0 to-green-500/0 group-hover:from-green-500/5 group-hover:to-emerald-500/5 transition-all duration-300"></div>
      <div class="relative">
        <div class="flex items-center justify-between mb-6 md:mb-8 gap-3">
          <h3 class="text-lg md:text-xl font-bold text-white">🎣 Phishing Findings</h3>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400 bg-slate-700/50 px-3 py-1.5 rounded-full">{{ phishing.findings.length }} findings</span>
        </div>
        <div v-if="phishing.findings.length === 0" class="text-slate-400 italic text-sm py-6">
          ✓ No phishing indicators detected
        </div>
        <ul v-else class="space-y-2 max-h-64 overflow-y-auto">
          <li 
            v-for="(finding, idx) in phishing.findings" 
            :key="`phishing-${idx}`"
            class="flex items-start gap-3 text-xs md:text-sm p-4 bg-gradient-to-r from-red-500/10 to-red-500/5 border border-red-500/20 hover:border-red-500/40 rounded-xl transition-all duration-300 group/item hover:bg-red-500/15"
          >
            <span class="text-lg flex-shrink-0 mt-0.5">⚠️</span>
            <span class="text-slate-200 group-hover/item:text-slate-100 break-words">{{ finding }}</span>
          </li>
        </ul>
      </div>
    </div>

    <!-- Spam Findings -->
    <div class="group relative overflow-hidden bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700/50 rounded-2xl p-6 md:p-8 hover:border-green-500/50 transition-all duration-300">
      <div class="absolute inset-0 bg-gradient-to-r from-green-500/0 to-green-500/0 group-hover:from-green-500/5 group-hover:to-emerald-500/5 transition-all duration-300"></div>
      <div class="relative">
        <div class="flex items-center justify-between mb-6 md:mb-8 gap-3">
          <h3 class="text-lg md:text-xl font-bold text-white">📧 Spam Findings</h3>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400 bg-slate-700/50 px-3 py-1.5 rounded-full">{{ spam.findings.length }} findings</span>
        </div>
        <div v-if="spam.findings.length === 0" class="text-slate-400 italic text-sm py-6">
          ✓ No spam indicators detected
        </div>
        <ul v-else class="space-y-2 max-h-64 overflow-y-auto">
          <li 
            v-for="(finding, idx) in spam.findings" 
            :key="`spam-${idx}`"
            class="flex items-start gap-3 text-xs md:text-sm p-4 bg-gradient-to-r from-orange-500/10 to-orange-500/5 border border-orange-500/20 hover:border-orange-500/40 rounded-xl transition-all duration-300 group/item hover:bg-orange-500/15"
          >
            <span class="text-lg flex-shrink-0 mt-0.5">🚩</span>
            <span class="text-slate-200 group-hover/item:text-slate-100 break-words">{{ finding }}</span>
          </li>
        </ul>
      </div>
    </div>

    <!-- Technical Details -->
    <div class="group relative overflow-hidden bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700/50 rounded-2xl p-6 md:p-8 hover:border-green-500/50 transition-all duration-300">
      <div class="absolute inset-0 bg-gradient-to-r from-green-500/0 to-green-500/0 group-hover:from-green-500/5 group-hover:to-emerald-500/5 transition-all duration-300"></div>
      <div class="relative">
        <h3 class="text-lg md:text-xl font-bold text-white mb-6 md:mb-8">📊 Technical Details</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6">
          <div class="bg-gradient-to-br from-blue-500/20 to-blue-500/10 border border-blue-500/20 rounded-xl p-4 hover:border-blue-500/50 transition-all duration-300">
            <p class="text-xs font-bold uppercase tracking-wider text-slate-400">URLs Found</p>
            <p class="text-white text-2xl md:text-3xl font-bold mt-2 md:mt-3">{{ metadata.url_count }}</p>
          </div>
          <div class="bg-gradient-to-br from-purple-500/20 to-purple-500/10 border border-purple-500/20 rounded-xl p-4 hover:border-purple-500/50 transition-all duration-300">
            <p class="text-xs font-bold uppercase tracking-wider text-slate-400">Attachments</p>
            <p class="text-white text-2xl md:text-3xl font-bold mt-2 md:mt-3">{{ metadata.attachment_count }}</p>
          </div>
          <div class="bg-gradient-to-br from-pink-500/20 to-pink-500/10 border border-pink-500/20 rounded-xl p-4 hover:border-pink-500/50 transition-all duration-300 md:col-span-2">
            <p class="text-xs font-bold uppercase tracking-wider text-slate-400">Classification</p>
            <p class="text-white text-sm md:text-base font-bold mt-2 md:mt-3 break-words">{{ classification }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  metadata: Object,
  phishing: Object,
  spam: Object,
  classification: String
})

const getPhishingColor = computed(() => {
  if (props.phishing.score >= 70) return 'text-red-400'
  if (props.phishing.score >= 50) return 'text-orange-400'
  if (props.phishing.score >= 30) return 'text-yellow-400'
  return 'text-green-400'
})

const getSpamColor = computed(() => {
  if (props.spam.score >= 80) return 'text-red-400'
  if (props.spam.score >= 50) return 'text-orange-400'
  if (props.spam.score >= 30) return 'text-yellow-400'
  return 'text-green-400'
})

const getPhishingBadgeClass = computed(() => {
  if (props.phishing.level === 'CRITICAL') return 'bg-red-500/30 text-red-200'
  if (props.phishing.level === 'HIGH') return 'bg-orange-500/30 text-orange-200'
  if (props.phishing.level === 'MEDIUM') return 'bg-yellow-500/30 text-yellow-200'
  if (props.phishing.level === 'LOW') return 'bg-blue-500/30 text-blue-200'
  return 'bg-green-500/30 text-green-200'
})

const getSpamBadgeClass = computed(() => {
  if (props.spam.level === 'LIKELY_SPAM') return 'bg-red-500/30 text-red-200'
  if (props.spam.level === 'SUSPICIOUS') return 'bg-orange-500/30 text-orange-200'
  if (props.spam.level === 'LOW_RISK') return 'bg-yellow-500/30 text-yellow-200'
  return 'bg-green-500/30 text-green-200'
})

const getPhishingGradient = computed(() => {
  if (props.phishing.score >= 70) return 'linear-gradient(90deg, #ef4444, #dc2626)'
  if (props.phishing.score >= 50) return 'linear-gradient(90deg, #f97316, #ea580c)'
  if (props.phishing.score >= 30) return 'linear-gradient(90deg, #eab308, #ca8a04)'
  return 'linear-gradient(90deg, #22c55e, #16a34a)'
})

const getSpamGradient = computed(() => {
  if (props.spam.score >= 80) return 'linear-gradient(90deg, #ef4444, #dc2626)'
  if (props.spam.score >= 50) return 'linear-gradient(90deg, #f97316, #ea580c)'
  if (props.spam.score >= 30) return 'linear-gradient(90deg, #eab308, #ca8a04)'
  return 'linear-gradient(90deg, #22c55e, #16a34a)'
})

const getRiskLevel = computed(() => {
  const score = Math.max(props.phishing.score, props.spam.score)
  if (score >= 70) return 'CRITICAL'
  if (score >= 50) return 'HIGH'
  if (score >= 30) return 'MEDIUM'
  return 'LOW'
})
</script>
