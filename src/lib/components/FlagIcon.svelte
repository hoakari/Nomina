<script lang="ts">
  let { code = 'en-US', size = 'md' } = $props<{
    code?: 'en-US' | 'en-GB' | 'zh-CN' | 'zh-TW' | 'es-ES' | 'es-MX' | 'fr-FR' | 'id-ID' | 'US' | 'GB' | 'CN' | 'TW' | 'ES' | 'MX' | 'FR' | 'ID';
    size?: 'sm' | 'md' | 'lg';
  }>();

  const sizeClasses = {
    sm: 'w-4 h-3 rounded-[2px]',
    md: 'w-7 h-5 rounded',
    lg: 'w-10 h-7 rounded-md'
  };

  const normCode = $derived(
    code === 'US' ? 'en-US' :
    code === 'GB' ? 'en-GB' :
    code === 'CN' ? 'zh-CN' :
    code === 'TW' ? 'zh-TW' :
    code === 'ES' ? 'es-ES' :
    code === 'MX' ? 'es-MX' :
    code === 'FR' ? 'fr-FR' :
    code === 'ID' ? 'id-ID' : code
  );
</script>

{#if normCode === 'en-US'}
  <!-- アメリカ国旗 SVG -->
  <svg class="inline-block shadow-sm overflow-hidden shrink-0 border border-slate-200/50 {sizeClasses[size]}" viewBox="0 0 741 390">
    <rect width="741" height="390" fill="#b22234"/>
    <path d="M0,30H741M0,90H741M0,150H741M0,210H741M0,270H741M0,330H741" stroke="#fff" stroke-width="30"/>
    <rect width="296.4" height="210" fill="#3c3b6e"/>
    <g fill="#fff">
      <g id="s18">
        <g id="s9">
          <g id="s5">
            <polygon id="s" points="11.4,0 14.1,8.3 22.8,8.3 15.8,13.4 18.5,21.7 11.4,16.6 4.3,21.7 7,13.4 0,8.3 8.7,8.3"/>
            <use href="#s" x="49.4"/>
            <use href="#s" x="98.8"/>
            <use href="#s" x="148.2"/>
            <use href="#s" x="197.6"/>
          </g>
          <use href="#s" x="247"/>
        </g>
        <g id="s4" x="24.7" y="17.5">
          <use href="#s" x="24.7" y="17.5"/>
          <use href="#s" x="74.1" y="17.5"/>
          <use href="#s" x="123.5" y="17.5"/>
          <use href="#s" x="172.9" y="17.5"/>
        </g>
      </g>
      <use href="#s18" y="35"/>
      <use href="#s18" y="70"/>
      <use href="#s18" y="105"/>
      <use href="#s5" y="140"/>
      <use href="#s4" y="140"/>
    </g>
  </svg>
{:else if normCode === 'en-GB'}
  <!-- イギリス国旗 (ユニオンジャック) SVG -->
  <svg class="inline-block shadow-sm overflow-hidden shrink-0 border border-slate-200/50 {sizeClasses[size]}" viewBox="0 0 60 30">
    <clipPath id="s">
      <path d="M0,0 v30 h60 v-30 z"/>
    </clipPath>
    <clipPath id="t">
      <path d="M30,15 H0 V0 z M30,15 V0 h30 z M30,15 H60 v15 z M30,15 V30 h-30 z"/>
    </clipPath>
    <g clip-path="url(#s)">
      <path d="M0,0 v30 h60 v-30 z" fill="#012169"/>
      <path d="M0,0 L60,30 M60,0 L0,30" stroke="#fff" stroke-width="6"/>
      <path d="M0,0 L60,30 M60,0 L0,30" stroke="#C8102E" stroke-width="2" clip-path="url(#t)"/>
      <path d="M30,0 v30 M0,15 h60" stroke="#fff" stroke-width="10"/>
      <path d="M30,0 v30 M0,15 h60" stroke="#C8102E" stroke-width="6"/>
    </g>
  </svg>
{:else if normCode === 'zh-CN'}
  <!-- 中国国旗 (五星紅旗) SVG -->
  <svg class="inline-block shadow-sm overflow-hidden shrink-0 border border-slate-200/50 {sizeClasses[size]}" viewBox="0 0 900 600">
    <rect width="900" height="600" fill="#ee1c25"/>
    <g fill="#ffde00">
      <polygon points="150,60 179,151 255,95 208,181 297,210 208,239 255,325 179,269 150,360 121,269 45,325 92,239 3,210 92,181 45,95 121,151"/>
      <polygon points="300,60 306,78 325,78 310,89 316,107 300,96 284,107 290,89 275,78 294,78" transform="rotate(23.036 300 60)"/>
      <polygon points="360,120 366,138 385,138 370,149 376,167 360,156 344,167 350,149 335,138 354,138" transform="rotate(45.869 360 120)"/>
      <polygon points="360,210 366,228 385,228 370,239 376,257 360,246 344,257 350,239 335,228 354,228" transform="rotate(69.944 360 210)"/>
      <polygon points="300,270 306,288 325,288 310,299 316,317 300,306 284,317 290,299 275,288 294,288" transform="rotate(98.130 300 270)"/>
    </g>
  </svg>
{:else if normCode === 'zh-TW'}
  <!-- 台湾国旗 (青天白日満地紅旗) SVG -->
  <svg class="inline-block shadow-sm overflow-hidden shrink-0 border border-slate-200/50 {sizeClasses[size]}" viewBox="0 0 900 600">
    <rect width="900" height="600" fill="#fe0000"/>
    <rect width="450" height="300" fill="#000095"/>
    <g transform="translate(225,150)">
      <circle r="75" fill="#fff"/>
      <g fill="#000095">
        <circle r="45"/>
      </g>
      <g fill="#fff">
        <polygon points="0,-112.5 16,-45 -16,-45"/>
        <polygon points="0,-112.5 16,-45 -16,-45" transform="rotate(30)"/>
        <polygon points="0,-112.5 16,-45 -16,-45" transform="rotate(60)"/>
        <polygon points="0,-112.5 16,-45 -16,-45" transform="rotate(90)"/>
        <polygon points="0,-112.5 16,-45 -16,-45" transform="rotate(120)"/>
        <polygon points="0,-112.5 16,-45 -16,-45" transform="rotate(150)"/>
        <polygon points="0,-112.5 16,-45 -16,-45" transform="rotate(180)"/>
        <polygon points="0,-112.5 16,-45 -16,-45" transform="rotate(210)"/>
        <polygon points="0,-112.5 16,-45 -16,-45" transform="rotate(240)"/>
        <polygon points="0,-112.5 16,-45 -16,-45" transform="rotate(270)"/>
        <polygon points="0,-112.5 16,-45 -16,-45" transform="rotate(300)"/>
        <polygon points="0,-112.5 16,-45 -16,-45" transform="rotate(330)"/>
      </g>
    </g>
  </svg>
{:else if normCode === 'es-ES'}
  <!-- スペイン国旗 SVG -->
  <svg class="inline-block shadow-sm overflow-hidden shrink-0 border border-slate-200/50 {sizeClasses[size]}" viewBox="0 0 750 500">
    <rect width="750" height="500" fill="#c60b1e"/>
    <rect y="125" width="750" height="250" fill="#ffc400"/>
    <g transform="translate(200, 250) scale(0.65)">
      <!-- 紋章の簡易シルエット表現 -->
      <rect x="-40" y="-50" width="80" height="100" rx="20" fill="#c60b1e" stroke="#000" stroke-width="4"/>
      <rect x="-36" y="-46" width="72" height="92" rx="18" fill="#ffc400"/>
      <path d="M-20,-30 H20 V30 H-20 Z" fill="#c60b1e"/>
      <circle cx="0" cy="-60" r="15" fill="#ffc400"/>
    </g>
  </svg>
{:else if normCode === 'es-MX'}
  <!-- メキシコ国旗 SVG -->
  <svg class="inline-block shadow-sm overflow-hidden shrink-0 border border-slate-200/50 {sizeClasses[size]}" viewBox="0 0 700 400">
    <rect width="233.3" height="400" fill="#006847"/>
    <rect x="233.3" width="233.3" height="400" fill="#fff"/>
    <rect x="466.6" width="233.3" height="400" fill="#ce1126"/>
    <g transform="translate(350, 200) scale(0.7)">
      <!-- 中央の紋章（鷲と蛇のシルエット） -->
      <circle r="45" fill="#8b5a2b"/>
      <path d="M-20,-10 C-10,-30 10,-30 20,-10 C10,20 -10,20 -20,-10 Z" fill="#006847"/>
      <circle cx="0" cy="-15" r="8" fill="#ce1126"/>
    </g>
  </svg>
{:else if normCode === 'fr-FR'}
  <!-- フランス国旗 (トリコロール 🇫🇷) SVG -->
  <svg class="inline-block shadow-sm overflow-hidden shrink-0 border border-slate-200/50 {sizeClasses[size]}" viewBox="0 0 900 600">
    <rect width="300" height="600" fill="#002395"/>
    <rect x="300" width="300" height="600" fill="#fff"/>
    <rect x="600" width="300" height="600" fill="#ed2939"/>
  </svg>
{:else if normCode === 'id-ID'}
  <!-- インドネシア国旗 (メラ・プティ 🇮🇩) SVG -->
  <svg class="inline-block shadow-sm overflow-hidden shrink-0 border border-slate-200/50 {sizeClasses[size]}" viewBox="0 0 900 600">
    <rect width="900" height="300" fill="#ce1126"/>
    <rect y="300" width="900" height="300" fill="#fff"/>
  </svg>
{/if}
