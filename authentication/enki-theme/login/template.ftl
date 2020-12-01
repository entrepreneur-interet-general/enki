<#macro registrationLayout bodyClass="" displayInfo=false displayMessage=true displayWide=false>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" class="${properties.kcHtmlClass!}">

<head>
  <meta charset="utf-8">
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="robots" content="noindex, nofollow">
  <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1" />

  <#if properties.meta?has_content>
    <#list properties.meta?split(' ') as meta>
      <meta name="${meta?split('==')[0]}" content="${meta?split('==')[1]}"/>
    </#list>
  </#if>
  <title>${msg("loginTitle",(realm.displayName!''))}</title>
  <link rel="icon" href="${url.resourcesPath}/img/favicon.ico" />
  <#if properties.styles?has_content>
    <#list properties.styles?split(' ') as style>
      <link href="${url.resourcesPath}/${style}" rel="stylesheet" />
    </#list>
  </#if>
  <#if properties.scripts?has_content>
    <#list properties.scripts?split(' ') as script>
      <script src="${url.resourcesPath}/${script}" type="text/javascript"></script>
    </#list>
  </#if>
  <#if scripts??>
    <#list scripts as script>
      <script src="${script}" type="text/javascript"></script>
    </#list>
  </#if>
</head>

<body class="${properties.kcBodyClass!}">
  <div class="login-container">
    <div class="login-background"></div>
    <div class="login-wrapper">
      <div class="login-form ${properties.kcFormCardClass!} <#if displayWide>${properties.kcFormCardAccountClass!}</#if>">
        <header class="form-header ${properties.kcFormHeaderClass!}">
          <img class="form-header__illus" src="${url.resourcesPath}/img/illus.png" />
          <img class="form-header__imgRepu" src="${url.resourcesPath}/img/Republique_Francaise.png" />
        </header>
        <div id="kc-content">
          <div id="kc-content-wrapper">

            <#-- App-initiated actions should not see warning messages about the need to complete the action -->
            <#-- during login.                                                                               -->
            <#if displayMessage && message?has_content && (message.type != 'warning' || !isAppInitiatedAction??)>
              <div class="alert alert-${message.type}">
                <#if message.type = 'success'><span class="${properties.kcFeedbackSuccessIcon!}"></span></#if>
                <#if message.type = 'warning'><span class="${properties.kcFeedbackWarningIcon!}"></span></#if>
                <#if message.type = 'error'><span class="${properties.kcFeedbackErrorIcon!}"></span></#if>
                <#if message.type = 'info'><span class="${properties.kcFeedbackInfoIcon!}"></span></#if>
                <span class="kc-feedback-text">${kcSanitize(message.summary)?no_esc}</span>
              </div>
            </#if>

            <#nested "form">

            <#if displayInfo>
              <div id="kc-info" class="${properties.kcSignUpClass!}">
                <div id="kc-info-wrapper" class="${properties.kcInfoAreaWrapperClass!}">
                    <#nested "info">
                </div>
              </div>
            </#if>
          </div>
        </div>
        <footer>
          <img class="form-footer__imgNexsis" src="${url.resourcesPath}/img/nexsis.svg" />
        </footer>
      </div>
    </div>
  </div>
</body>
</html>
</#macro>
