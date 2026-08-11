/**
 * Web Audio API を用いて録音データの前後の無音部分（小音量部分）を爆速自動トリミングするユーティリティ
 */

export async function trimSilenceFromAudioBlob(inputBlob: Blob, threshold = 0.015, paddingSec = 0.05): Promise<Blob> {
  if (!inputBlob || inputBlob.size === 0) return inputBlob;

  try {
    const arrayBuffer = await inputBlob.arrayBuffer();
    const AudioContextClass = window.AudioContext || (window as any).webkitAudioContext;
    if (!AudioContextClass) return inputBlob;

    // 軽量な AudioContext
    const audioCtx = new AudioContextClass();
    
    let audioBuffer: AudioBuffer;
    try {
      audioBuffer = await audioCtx.decodeAudioData(arrayBuffer);
    } catch (decodeErr) {
      await audioCtx.close();
      return inputBlob;
    }

    const numberOfChannels = audioBuffer.numberOfChannels;
    const sampleRate = audioBuffer.sampleRate;
    const length = audioBuffer.length;

    if (length === 0) {
      await audioCtx.close();
      return inputBlob;
    }

    // 128サンプル（約2.6ms）刻みで超高速スキャン
    const step = 128;
    let startIndex = 0;
    let endIndex = length - 1;

    // 先頭の無音検出
    findStart: for (let i = 0; i < length; i += step) {
      for (let ch = 0; ch < numberOfChannels; ch++) {
        const sampleData = audioBuffer.getChannelData(ch);
        if (Math.abs(sampleData[i]) > threshold) {
          startIndex = i;
          break findStart;
        }
      }
    }

    // 末尾の無音検出
    findEnd: for (let i = length - 1; i >= startIndex; i -= step) {
      for (let ch = 0; ch < numberOfChannels; ch++) {
        const sampleData = audioBuffer.getChannelData(ch);
        if (Math.abs(sampleData[i]) > threshold) {
          endIndex = i;
          break findEnd;
        }
      }
    }

    // パディング調整
    const paddingSamples = Math.floor(sampleRate * paddingSec);
    startIndex = Math.max(0, startIndex - paddingSamples);
    endIndex = Math.min(length - 1, endIndex + paddingSamples);

    const trimmedLength = endIndex - startIndex + 1;
    if (trimmedLength <= 0 || trimmedLength >= length) {
      await audioCtx.close();
      return inputBlob;
    }

    // 高速切出
    const trimmedBuffer = audioCtx.createBuffer(numberOfChannels, trimmedLength, sampleRate);
    for (let ch = 0; ch < numberOfChannels; ch++) {
      const srcChannel = audioBuffer.getChannelData(ch);
      const destChannel = trimmedBuffer.getChannelData(ch);
      destChannel.set(srcChannel.subarray(startIndex, endIndex + 1));
    }

    // 高速 WAV エンコード
    const wavBlob = audioBufferToWavFast(trimmedBuffer);
    await audioCtx.close();
    return wavBlob;
  } catch (err) {
    console.warn('Audio trimming fallback:', err);
    return inputBlob;
  }
}

/**
 * 爆速 WAV エンコーダー
 */
function audioBufferToWavFast(buffer: AudioBuffer): Blob {
  const numChannels = buffer.numberOfChannels;
  const sampleRate = buffer.sampleRate;
  const length = buffer.length;
  const bytesPerSample = 2; // 16-bit
  const blockAlign = numChannels * bytesPerSample;
  const dataLength = length * blockAlign;

  const arrayBuffer = new ArrayBuffer(44 + dataLength);
  const view = new DataView(arrayBuffer);

  /* RIFF header */
  writeString(view, 0, 'RIFF');
  view.setUint32(4, 36 + dataLength, true);
  writeString(view, 8, 'WAVE');
  writeString(view, 12, 'fmt ');
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true); // PCM
  view.setUint16(22, numChannels, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * blockAlign, true);
  view.setUint16(32, blockAlign, true);
  view.setUint16(34, 16, true);
  writeString(view, 36, 'data');
  view.setUint32(40, dataLength, true);

  // チャンネルデータを高速インタリーブ変換
  const channels: Float32Array[] = [];
  for (let c = 0; c < numChannels; c++) {
    channels.push(buffer.getChannelData(c));
  }

  let offset = 44;
  for (let i = 0; i < length; i++) {
    for (let c = 0; c < numChannels; c++) {
      const s = Math.max(-1, Math.min(1, channels[c][i]));
      const val = s < 0 ? s * 0x8000 : s * 0x7fff;
      view.setInt16(offset, val, true);
      offset += 2;
    }
  }

  return new Blob([arrayBuffer], { type: 'audio/wav' });
}

function writeString(view: DataView, offset: number, string: string) {
  for (let i = 0; i < string.length; i++) {
    view.setUint8(offset + i, string.charCodeAt(i));
  }
}
