<#import "template.ftl" as layout>
<@layout.registrationLayout; section>
  <#if section = "title">
    ${msg("loginTitle",realm.name)}
  <#elseif section = "header">
    ${msg("loginTitleHtml",realm.name)}
  <#elseif section = "form">
    <form id="kc-totp-login-form" class="${properties.kcFormClass!}" action="${url.loginAction}" method="post">
      <#if rolesBySis?? && rolesBySis?has_content>
        <p>Quel est votre rôle ?</p>
      <#list rolesBySis as rolesAndSis>
        <h2> ${rolesAndSis.sis.nom}</h2>
        <#list rolesAndSis.roles>
          <ul>
          <#items as role>
              <li><label for="${role.id}"><input type="radio" name="nexsis-role" value="${role.id}"
                                                 id="${role.id}"/>${role.uniteFonctionnelle.nom} - ${role.profil.nom}</label></li>
          </#items>
          </ul>
        </#list>
      </#list>
      </#if>
      <div class="${properties.kcFormGroupClass!}">

        <div id="kc-form-buttons" class="${properties.kcFormButtonsClass!}">
          <div class="${properties.kcFormButtonsWrapperClass!}">
            <#if !message?has_content>
            <input
              class="${properties.kcButtonClass!} ${properties.kcButtonPrimaryClass!} ${properties.kcButtonLargeClass!}"
              name="login" id="kc-login" type="submit" value="${msg("doLogIn")}"/>
              </#if>
            <#if message?has_content>
            <input  class="${properties.kcButtonClass!} ${properties.kcButtonDefaultClass!} ${properties.kcButtonLargeClass!}"
                   name="cancel" id="kc-cancel" type="submit" value="${msg("doCancel")}"/>
            </#if>
          </div>
        </div>
      </div>
    </form>
  </#if>
</@layout.registrationLayout>
