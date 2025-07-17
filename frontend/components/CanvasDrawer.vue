<template>
  <div class="flex flex-col gap-4"> <!-- g-1rem -> gap-4 -->
    <canvas
      ref="canvas"
      width="280"
      height="280"
      class="border draw-area"
      @pointerdown="startDraw"
      @pointermove="onDraw"
      @pointerup="endDraw"
      @pointerleave="endDraw"
      @pointercancel="endDraw"
    />
    <div class="flex gap-20">                      <!-- g-5rem -> gap-20 (約5rem相当) -->
      <button
        @click="clearCanvas"
        :disabled="busy"
        class="p-1 bg-blue-300 mt-2 mb-2 mr-2 text-[20px] disabled:opacity-50 disabled:cursor-not-allowed"
      >クリア</button>
      <button
        @click="predict"
        :disabled="busy"
        class="pt-1 pb-1 pr-1 pl-2 bg-green-300 m-2 text-[20px] disabled:opacity-50 disabled:cursor-not-allowed"
      >GO！</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import axios from 'axios'

/**
 * Emits:
 *  - result({ digits:number[], probs:number[] })
 *  - clear()
 *  - thinking(boolean)
 */
const emit = defineEmits(['result', 'clear', 'thinking'])

const canvas = ref(null)
let ctx
let drawing = false
const busy = ref(false)                // ★ リクエスト中ボタン無効

/* ------------------------------
   グローバル touchmove ブロッカー
   （描画中にページがスクロールしないよう一時登録）
-------------------------------- */
let activeTouchBlocker = null
function addGlobalTouchBlocker () {    // ★
  if (activeTouchBlocker) return
  activeTouchBlocker = (e) => {
    if (e.touches?.length) e.preventDefault()
  }
  document.addEventListener('touchmove', activeTouchBlocker, { passive: false })
}
function removeGlobalTouchBlocker () { // ★
  if (!activeTouchBlocker) return
  document.removeEventListener('touchmove', activeTouchBlocker, { passive: false })
  activeTouchBlocker = null
}

onMounted(() => {
  ctx = canvas.value.getContext('2d')
  initCanvas()
})
onBeforeUnmount(() => {                 // ★ 後片付け
  removeGlobalTouchBlocker()
})

function initCanvas () {
  const c = canvas.value
  ctx.fillStyle = 'black'
  ctx.fillRect(0, 0, c.width, c.height)
  ctx.strokeStyle = 'white'
  ctx.lineWidth = 10
  ctx.lineCap = 'round'
}

function startDraw (e) {
  drawing = true
  e.preventDefault()
  try { canvas.value.setPointerCapture(e.pointerId) } catch {}  // ★ .value
  addGlobalTouchBlocker()                                        // ★ スクロールロック
  ctx.beginPath()
  ctx.moveTo(e.offsetX, e.offsetY)
}

function onDraw (e) {
  if (!drawing) return
  e.preventDefault()
  ctx.lineTo(e.offsetX, e.offsetY)
  ctx.stroke()
}

function endDraw (e) {
  if (!drawing) return
  drawing = false
  e?.preventDefault?.()
  try { canvas.value.releasePointerCapture(e.pointerId) } catch {} // ★ .value
  removeGlobalTouchBlocker()                                       // ★ ロック解除
}

function clearCanvas () {
  const c = canvas.value
  ctx.fillStyle = 'black'
  ctx.fillRect(0, 0, c.width, c.height)
  emit('clear')
}

async function predict () {
  if (busy.value) return
  busy.value = true

  emit('thinking', true)      // ★ 通信前にすぐ表示
  const dataUrl = canvas.value.toDataURL('image/png')

  try {
    const { data } = await axios.post(
      'https://mnist-recognition.onrender.com/predict',
      { image: dataUrl },
      { timeout: 30000 }
    )

    // 演出待ち（7.5s）
    await new Promise(r => setTimeout(r, 7500))

    emit('result', { digits: data.digits, probs: data.probs })

  } catch (error) {
    console.error(error)
    alert('予測に失敗しました')

  } finally {
    emit('thinking', false)   // ★ 必ずオフ
    busy.value = false
    // clearCanvas()           // 必要なら開放
  }
}
</script>

<style scoped>
/* 元 CSS 調整・統合版 */

canvas.border {
  border: 1px solid #ccc;
  cursor: crosshair;
}

/* キャンバスだけスクロール無効 */
.draw-area {
  touch-action: none;          /* スクロール・ズームをブロック */
  -ms-touch-action: none;
  overscroll-behavior: contain;/* スクロール連鎖を止める */
}

/* 任意: 親コンテナのスクロール連鎖も遮断したい場合 */
.canvas-wrapper {
  overscroll-behavior: contain;
}
</style>
