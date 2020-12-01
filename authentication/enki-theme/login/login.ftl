<#import "template.ftl" as layout>
<@layout.registrationLayout displayInfo=social.displayInfo displayWide=(realm.password && social.providers??); section>
  <#if section = "header">
    ${msg("doLogIn")}
  <#elseif section = "form">
  <div class="title-container">
    <h1 class="login-title">Bienvenue sur ENKI</h1>
    <p class="login-subtitle">Première visite ? <a href="${url.registrationUrl}" class="login-signupLink">Créer un compte</a>
  </div>
  <div id="kc-form" <#if realm.password && social.providers??>class="${properties.kcContentWrapperClass!}"</#if>>
    <div id="kc-form-wrapper" <#if realm.password && social.providers??>class="${properties.kcFormSocialAccountContentClass!} ${properties.kcFormSocialAccountClass!}"</#if>>
      <#if realm.password>
        <form id="kc-form-login" onsubmit="login.disabled = true; return true;" action="${url.loginAction}" method="post" novalidate>
          <div class="form-group">
            <#if usernameEditDisabled??>
              <input tabindex="1" id="username" class="js-loginInputs ${properties.kcInputClass!}" name="username" value="${(login.username!'')}"  type="text" disabled />
            <#else>
              <input tabindex="1" id="username" class="js-loginInputs ${properties.kcInputClass!}" name="username" value="${(login.username!'')}" required type="text" autofocus autocomplete="off" />
            </#if>
            <label for="username" class="form-control"><#if !realm.loginWithEmailAllowed>${msg("username")}<#elseif !realm.registrationEmailAsUsername>${msg("usernameOrEmail")}<#else>${msg("email")}</#if></label>
          </div>

          <div class="form-group">
            <input tabindex="2" id="password" class="js-loginInputs ${properties.kcInputClass!}" name="password" type="password" autocomplete="off" required />
            <label for="password" class="form-control">${msg("password")}</label>
            <div class="js-showPwd show-password"></div>
          </div>

          <div class="${properties.kcFormGroupClass!} ${properties.kcFormSettingClass!}">
            <div id="kc-form-options">
              <#if realm.rememberMe && !usernameEditDisabled??>
                <div class="checkbox">
                  <label>
                    <#if login.rememberMe??>
                      <input placeholder="totoot" tabindex="3" id="rememberMe" name="rememberMe" type="checkbox" checked> ${msg("rememberMe")}
                    <#else>
                      <input tabindex="3" id="rememberMe" name="rememberMe" type="checkbox"> ${msg("rememberMe")}
                    </#if>
                  </label>
                </div>
              </#if>
              </div>
            </div>

            <div id="kc-form-buttons" class="${properties.kcFormGroupClass!}">
                <input type="hidden" id="id-hidden-input" name="credentialId" <#if auth.selectedCredential?has_content>value="${auth.selectedCredential}"</#if>/>
                <input tabindex="4" class="${properties.kcButtonClass!} ${properties.kcButtonPrimaryClass!} ${properties.kcButtonBlockClass!} ${properties.kcButtonLargeClass!}" name="login" id="kc-login" type="submit" value="${msg("doLogIn")}" disabled/>
            </div>
            <div class="login-reset-password">
              <#if realm.resetPasswordAllowed>
                <a tabindex="5" href="${url.loginResetCredentialsUrl}">${msg("doForgotPassword")}</a>
              </#if>
            </div>
        </form>
      </#if>
      </div>
      <#if realm.password && social.providers??>
        <div id="kc-social-providers" class="${properties.kcFormSocialAccountContentClass!} ${properties.kcFormSocialAccountClass!}">
          <ul class="${properties.kcFormSocialAccountListClass!} <#if social.providers?size gt 4>${properties.kcFormSocialAccountDoubleListClass!}</#if>">
            <#list social.providers as p>
              <li class="${properties.kcFormSocialAccountListLinkClass!}"><a href="${p.loginUrl}" id="zocial-${p.alias}" class="zocial ${p.providerId}"> <span>${p.displayName}</span></a></li>
            </#list>
          </ul>
        </div>
      </#if>
    </div>
  <#elseif section = "info" >
    <#--  <#if realm.password && realm.registrationAllowed && !usernameEditDisabled??>
      <div id="kc-registration">
        <span>${msg("noAccount")} <a tabindex="6" href="${url.registrationUrl}">${msg("doRegister")}</a></span>
      </div>
    </#if>  -->
  </#if>

</@layout.registrationLayout>
