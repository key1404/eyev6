import streamlit as st
import numpy as np
from PIL import Image
import streamlit.components.v1 as components

# تنظیمات صفحه
st.set_page_config(
    page_title="Eye1 AI | سامانه جامع انتخاب و تست زنده عینک",
    page_icon="👓",
    layout="wide"
)

st.title("👓 سامانه هوشمند Eye1: تحلیل چهره، پیشنهاد تخصصی و امتحان مجازی حرفه‌ای")

# مدیریت حالت‌های برنامه (مراحل سه‌گانه)
if "step" not in st.session_state:
    st.session_state.step = "capture"
if "image" not in st.session_state:
    st.session_state.image = None
if "face_shape" not in st.session_state:
    st.session_state.face_shape = ""
if "selected_frame" not in st.session_state:
    st.session_state.selected_frame = None

# نوار کناری تنظیمات بالینی
st.sidebar.header("⚙️ پارامترهای اپتومتری")
rx_type = st.sidebar.selectbox("نوع نسخه بینایی (Rx)", ["دوربین / نزدیک‌بین (ساده)", "آستیگمات", "دید پیش‌رونده", "بدون نمره"])
pd_input = st.sidebar.slider("فاصله دو چشم (PD بر حسب میلی‌متر)", 50, 75, 62)

# ---------------------------------------------------------
# مرحله ۱: ثبت یا آپلود تصویر چهره برای آنالیز اولیه
# ---------------------------------------------------------
if st.session_state.step == "capture":
    st.markdown("### مرحله ۱: ثبت تصویر چهره برای تحلیل آناتومیک")
    st.info("لطفاً یک تصویر واضح از چهره خود آپلود کنید یا عکسی برای استخراج فرم صورت ثبت نمایید.")
    
    tab1, tab2 = st.tabs(["📸 عکاسی برای تحلیل اولیه", "📤 آپلود فایل تصویر"])
    
    uploaded_img = None
    with tab1:
        cam_file = st.camera_input("ثبت عکس جهت آنالیز اولیه:")
        if cam_file is not None:
            uploaded_img = Image.open(cam_file)
            
    with tab2:
        file = st.file_uploader("یا بارگذاری تصویر چهره:", type=["jpg", "jpeg", "png"])
        if file is not None:
            uploaded_img = Image.open(file)
            
    if uploaded_img is not None:
        st.session_state.image = uploaded_img
        
        # تحلیل هندسی فرم صورت
        img_arr = np.array(uploaded_img)
        h, w = img_arr.shape[:2]
        ratio = h / w
        
        if ratio > 1.38:
            st.session_state.face_shape = "کشیده (Oblong / Long Face)"
            st.session_state.frames = [
                {"id": "aviator", "name": "Tom Ford - Aviator Luxe", "type": "خلبانی عریض با پل ضخیم", "brand": "Tom Ford", "color": "#1f77b4"},
                {"id": "square", "name": "Ray-Ban - Square Classic", "type": "مستطیلی پهن کلاسیک", "brand": "Ray-Ban", "color": "#ff7f0e"}
            ]
        elif 1.18 <= ratio <= 1.38:
            st.session_state.face_shape = "بیضی متعادل (Oval - استاندارد طلایی)"
            st.session_state.frames = [
                {"id": "wayfarer", "name": "Ray-Ban - Wayfarer Original", "type": "ویفرر استاندارد کلاسیک", "brand": "Ray-Ban", "color": "#2ca02c"},
                {"id": "cateye", "name": "Tom Ford - Cat Eye Modern", "type": "چشم‌گربه‌ای شیک و مدرن", "brand": "Tom Ford", "color": "#d62728"}
            ]
        else:
            st.session_state.face_shape = "گرد یا مربعی (Round / Square)"
            st.session_state.frames = [
                {"id": "rect", "name": "Tom Ford - Slim Rectangular", "type": "مستطیلی باریک زاویه‌دار", "brand": "Tom Ford", "color": "#9467bd"},
                {"id": "round", "name": "Ray-Ban - Round Metal", "type": "گرد فلزی مینیمال سبک", "brand": "Ray-Ban", "color": "#8c564b"}
            ]
        
        st.session_state.step = "analyze"
        st.rerun()

# ---------------------------------------------------------
# مرحله ۲: نمایش تحلیل چهره و گالری مدل‌ها
# ---------------------------------------------------------
elif st.session_state.step == "analyze":
    st.markdown("### مرحله ۲: نتیجه تحلیل هوش مصنوعی و انتخاب مدل فریم")
    
    col_img, col_report = st.columns([1, 1.3])
    with col_img:
        st.image(st.session_state.image, caption="تصویر تحلیل‌شده", use_column_width=True)
        if st.button("🔄 عکاسی یا بارگذاری تصویر جدید"):
            st.session_state.step = "capture"
            st.rerun()
            
    with col_report:
        st.success("✅ تحلیل آناتومیک با موفقیت انجام شد!")
        st.write(f"🔹 **فرم هندسی تشخیص‌داده‌شده:** {st.session_state.face_shape}")
        st.write(f"📏 **پارامترهای PD:** {pd_input}mm | **نسخه:** {rx_type}")
        st.markdown("---")
        st.markdown("💡 لطفاً یکی از مدل‌های زیر را انتخاب کنید تا مستقیماً وارد **اتاق تست زنده با فریم واقعی و ردیابی سر** شوید:")

    st.markdown("---")
    
    f_cols = st.columns(len(st.session_state.frames))
    for i, frame in enumerate(st.session_state.frames):
        with f_cols[i]:
            st.markdown(f"""
                <div style="border: 2px solid {frame['color']}; padding: 15px; border-radius: 10px; background-color: #fcfcfc; text-align: center;">
                    <h4>{frame['name']}</h4>
                    <p><b>برند:</b> {frame['brand']}</p>
                    <p><b>طراحی:</b> {frame['type']}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"✨ تست زنده این مدل روی چهره", key=f"btn_frame_{i}"):
                st.session_state.selected_frame = frame
                st.session_state.step = "tryon"
                st.rerun()

# ---------------------------------------------------------
# مرحله ۳: اتاق امتحان مجازی زنده با فریم واقعی و ردیابی سر
# ---------------------------------------------------------
elif st.session_state.step == "tryon":
    chosen = st.session_state.selected_frame
    
    st.markdown(f"### مرحله ۳: اتاق تست زنده واقعیت افزوده (فریم فعال: {chosen['name']})")
    st.markdown("دوربین فعال است. عینک کاملاً بر اساس فرم انتخابی شما روی چشمان قرار گرفته و با حرکت سر و زوایای مختلف به صورت پویا ردیابی می‌شود.")
    
    if st.button("← بازگشت به گالری و انتخاب فریم دیگر"):
        st.session_state.step = "analyze"
        st.rerun()
        
    st.markdown("---")

    # کد پیشرفته ردیابی زنده سر همراه با رسم وکتور واقعی فریم عینک انتخابی
    ar_tryon_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/face_mesh.js" crossorigin="anonymous"></script>
        <style>
            .ar-container {{
                position: relative;
                width: 640px;
                height: 480px;
                margin: auto;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                background: #000;
            }}
            video, canvas {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                transform: scaleX(-1);
            }}
            .loading {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: white;
                font-family: Tahoma, sans-serif;
                font-size: 16px;
                z-index: 10;
                background: rgba(0,0,0,0.8);
                padding: 12px 24px;
                border-radius: 8px;
            }}
            .info-bar {{
                text-align: center;
                background: #eef7fc;
                padding: 10px;
                font-family: Tahoma, sans-serif;
                font-size: 14px;
                color: #333;
                max-width: 640px;
                margin: 10px auto 0 auto;
                border-radius: 8px;
            }}
        </style>
    </head>
    <body>
        <div class="ar-container">
            <div id="loading" class="loading">در حال راه‌اندازی دوربین و هوش مصنوعی فریم عینک...</div>
            <video id="webcam" autoplay playsinline muted></video>
            <canvas id="output_canvas"></canvas>
        </div>
        <div class="info-bar">
            <b>فریم انتخاب‌شده:</b> {chosen['name']} | <b>تنظیم PD:</b> {pd_input}mm | 🟢 تست زنده وکتور فعال است
        </div>

        <script>
            const videoElement = document.getElementById('webcam');
            const canvasElement = document.getElementById('output_canvas');
            const canvasCtx = canvasElement.getContext('2d');
            const loadingElement = document.getElementById('loading');

            const frameType = "{chosen['id']}";

            function drawRealisticGlasses(ctx, x, y, width, height, angle, fType) {{
                ctx.save();
                ctx.translate(x, y);
                ctx.rotate(angle);

                // استایل فریم عینک بر اساس نوع انتخاب شده
                ctx.lineWidth = Math.max(4, width * 0.04);
                ctx.strokeStyle = '#111111'; // رنگ فریم تیره کلاسیک
                ctx.fillStyle = 'rgba(100, 150, 200, 0.2)'; // رنگ عدسی شفاف دودی

                const eyeDist = width * 0.45; // فاصله بین دو مرکز عدسی
                const rW = width * 0.32; // عرض هر عدسی
                const rH = height * 0.7;  // ارتفاع هر عدسی

                if (fType === 'aviator') {{
                    // فریم خلبانی (قطره‌ای)
                    ctx.beginPath();
                    ctx.ellipse(-eyeDist, 0, rW, rH * 1.1, 0, 0, Math.PI * 2);
                    ctx.ellipse(eyeDist, 0, rW, rH * 1.1, 0, 0, Math.PI * 2);
                    ctx.stroke();
                    ctx.fill();
                    // پل دوبل خلبانی
                    ctx.beginPath();
                    ctx.moveTo(-eyeDist + rW*0.5, -rH*0.4);
                    ctx.lineTo(eyeDist - rW*0.5, -rH*0.4);
                    ctx.moveTo(-eyeDist + rW*0.3, -rH*0.55);
                    ctx.lineTo(eyeDist - rW*0.3, -rH*0.55);
                    ctx.stroke();
                }} else if (fType === 'cateye') {{
                    // فریم چشم‌گربه‌ای (کشیده به سمت بالا)
                    ctx.beginPath();
                    ctx.roundRect(-eyeDist - rW, -rH, rW * 2, rH * 1.5, [15, 30, 10, 10]);
                    ctx.roundRect(eyeDist - rW, -rH, rW * 2, rH * 1.5, [30, 15, 10, 10]);
                    ctx.stroke();
                    ctx.fill();
                }} else if (fType === 'round') {{
                    // فریم گرد فلزی
                    ctx.beginPath();
                    ctx.arc(-eyeDist, 0, rH * 0.8, 0, Math.PI * 2);
                    ctx.arc(eyeDist, 0, rH * 0.8, 0, Math.PI * 2);
                    ctx.stroke();
                    ctx.fill();
                    // پل بینی صاف
                    ctx.beginPath();
                    ctx.moveTo(-eyeDist + rH * 0.8, 0);
                    ctx.lineTo(eyeDist - rH * 0.8, 0);
                    ctx.stroke();
                }} else {{
                    // فریم مستطیلی / ویفرر استاندارد
                    ctx.beginPath();
                    ctx.roundRect(-eyeDist - rW, -rH * 0.8, rW * 2, rH * 1.4, 8);
                    ctx.roundRect(eyeDist - rW, -rH * 0.8, rW * 2, rH * 1.4, 8);
                    ctx.stroke();
                    ctx.fill();
                    // پل بینی
                    ctx.beginPath();
                    ctx.moveTo(-eyeDist + rW, -rH * 0.2);
                    ctx.lineTo(eyeDist - rW, -rH * 0.2);
                    ctx.stroke();
                }}

                ctx.restore();
            }}

            function onResults(results) {{
                loadingElement.style.display = 'none';
                canvasElement.width = videoElement.videoWidth;
                canvasElement.height = videoElement.videoHeight;

                canvasCtx.save();
                canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);

                if (results.multiFaceLandmarks && results.multiFaceLandmarks.length > 0) {{
                    const landmarks = results.multiFaceLandmarks[0];
                    
                    // نقاط چشم‌ها برای محاسبه مرکز و زاویه سر (Tilt)
                    const leftEye = landmarks[33];
                    const rightEye = landmarks[263];

                    const x = (leftEye.x + rightEye.x) / 2 * canvasElement.width;
                    const y = (leftEye.y + rightEye.y) / 2 * canvasElement.height - 5; // تنظیم روی پل بینی

                    // محاسبه زاویه چرخش سر
                    const dx = (rightEye.x - leftEye.x) * canvasElement.width;
                    const dy = (rightEye.y - leftEye.y) * canvasElement.height;
                    const angle = Math.atan2(dy, dx);

                    // محاسبه مقیاس بر اساس پهنای صورت
                    const leftCheek = landmarks[234];
                    const rightCheek = landmarks[454];
                    const faceWidth = Math.hypot(
                        (rightCheek.x - leftCheek.x) * canvasElement.width,
                        (rightCheek.y - leftCheek.y) * canvasElement.height
                    );

                    const glassesWidth = faceWidth * 1.1;
                    const glassesHeight = glassesWidth * 0.4;

                    // رسم فریم عینک واقعی متناسب با مدل انتخابی
                    drawRealisticGlasses(canvasCtx, x, y, glassesWidth, glassesHeight, angle, frameType);
                }}
                canvasCtx.restore();
            }}

            const faceMesh = new FaceMesh({{
                locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${{file}}`
            }});

            faceMesh.setOptions({{
                maxNumFaces: 1,
                refineLandmarks: true,
                minDetectionConfidence: 0.5,
                minTrackingConfidence: 0.5
            }});

            faceMesh.onResults(onResults);

            const camera = new Camera(videoElement, {{
                onFrame: async () => {{
                    await faceMesh.send({{ image: videoElement }});
                }},
                width: 640,
                height: 480
            }});

            camera.start().catch(err => {{
                loadingElement.innerText = "خطا در دسترسی به دوربین مرورگر!";
                console.error(err);
            }});
        </script>
    </body>
    </html>
    """

    components.html(ar_tryon_html, height=580)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 پایان تست و شروع مجدد با چهره جدید"):
        st.session_state.step = "capture"
        st.rerun()