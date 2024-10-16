import os
import json
import streamlit as st

def patch_head(document, content):
    return document.replace('<head>', '<head>' + content)

def patch_body(document, content):
    return document.replace('<body>', '<body>' + content)

def google_analytics_head(gtm_tag):
    return f"""
        <script>
        // Define dataLayer and the gtag function.
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}

        // Set default consent to 'denied' as a placeholder
        // Determine actual values based on your own requirements
        gtag('consent', 'default', {{
            'ad_storage': 'denied',
            'ad_user_data': 'denied',
            'ad_personalization': 'denied',
            'analytics_storage': 'denied'
        }});
        </script>
        <!-- Google Tag Manager -->
        <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
        new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
        j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
        'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
        }})(window,document,'script','dataLayer','{gtm_tag}');</script>
        <!-- End Google Tag Manager -->
    """

def google_analytics_body(gtm_tag):
    return f"""
        <!-- Google Tag Manager (noscript) -->
        <noscript><iframe src="https://www.googletagmanager.com/ns.html?id={gtm_tag}"
        height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
        <!-- End Google Tag Manager (noscript) -->
    """


if __name__ == '__main__':
    
    # Load configuration
    settings_path = os.path.join(os.path.dirname(__file__), '..', 'settings.json')
    with open(settings_path, 'r') as f:
        settings = json.load(f)

    # Load index.html
    index_path = os.path.join(os.path.dirname(st.__file__), 'static', 'index.html')
    with open(index_path, 'r') as f:
        index = f.read()
    
    # Configure google analytics
    if settings['analytics']['google_analytics']['enabled']:
        gtm_tag = settings['analytics']['google_analytics']['tag']
        index = patch_head(index, google_analytics_head(gtm_tag))
        index = patch_body(index, google_analytics_body(gtm_tag))
    
    # Save index.html
    with open(index_path, 'w') as f:
        f.write(index)