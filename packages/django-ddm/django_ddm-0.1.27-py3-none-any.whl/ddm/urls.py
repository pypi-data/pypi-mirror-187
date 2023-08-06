from django.urls import path, include

from ddm.views import project_admin, participation_flow
from ddm.views.exception_api import ExceptionAPI
from ddm.views.download import DownloadProjectDataView


participation_flow_patterns = [
    path(r'intro/', participation_flow.EntryView.as_view(), name='project-entry'),
    path(r'data-donation/', participation_flow.DataDonationView.as_view(), name='data-donation'),
    path(r'questionnaire/', participation_flow.QuestionnaireView.as_view(), name='questionnaire'),
    path(r'end/', participation_flow.ExitView.as_view(), name='project-exit')
]

question_patterns = [
    path(r'', project_admin.QuestionnaireOverview.as_view(), name='questionnaire-overview'),
    path(r'<slug:question_type>/create/', project_admin.QuestionCreate.as_view(), name='question-create'),
    path(r'<slug:question_type>/<int:pk>/edit/', project_admin.QuestionEdit.as_view(), name='question-edit'),
    path(r'<slug:question_type>/<int:pk>/delete/', project_admin.QuestionDelete.as_view(), name='question-delete'),
    path(r'<slug:question_type>/<int:pk>/items/', project_admin.ItemEdit.as_view(), name='question-items'),
    path(r'<slug:question_type>/<int:pk>/scale/', project_admin.ScaleEdit.as_view(), name='question-scale'),
]

instruction_patterns = [
    path(r'', project_admin.InstructionOverview.as_view(), name='instruction-overview'),
    path(r'create/', project_admin.InstructionCreate.as_view(), name='instruction-create'),
    path(r'<int:pk>/edit/', project_admin.InstructionEdit.as_view(), name='instruction-edit'),
    path(r'<int:pk>/delete/', project_admin.InstructionDelete.as_view(), name='instruction-delete'),
]

blueprint_patterns = [
    path(r'', project_admin.data_donations.ProjectBlueprintList.as_view(), name='blueprint-list'),
    path(r'blueprint/create/', project_admin.BlueprintCreate.as_view(), name='blueprint-create'),
    path(r'blueprint/<int:pk>/edit/', project_admin.BlueprintEdit.as_view(), name='blueprint-edit'),
    path(r'blueprint/<int:pk>/delete/', project_admin.BlueprintDelete.as_view(), name='blueprint-delete'),
    path(r'zip-blueprint/create/', project_admin.ZippedBlueprintCreate.as_view(), name='zipped-blueprint-create'),
    path(r'zip-blueprint/<int:pk>/edit/', project_admin.ZippedBlueprintEdit.as_view(), name='zipped-blueprint-edit'),
    path(r'zip-blueprint/<int:pk>/delete/', project_admin.ZippedBlueprintDelete.as_view(), name='zipped-blueprint-delete'),
    path(r'<slug:blueprint_type>/<int:blueprint_pk>/instructions/', include(instruction_patterns)),
]

project_admin_patterns = [
    path(r'', project_admin.ProjectList.as_view(), name='project-list'),
    path(r'create/', project_admin.ProjectCreate.as_view(), name='project-create'),
    path(r'<int:pk>/', project_admin.ProjectDetail.as_view(), name='project-detail'),
    path(r'<int:pk>/edit/', project_admin.ProjectEdit.as_view(), name='project-edit'),
    path(r'<int:pk>/delete/', project_admin.ProjectDelete.as_view(), name='project-delete'),
    path(r'<int:pk>/welcome-page/', project_admin.WelcomePageEdit.as_view(), name='welcome-page-edit'),
    path(r'<int:pk>/end-page/', project_admin.EndPageEdit.as_view(), name='end-page-edit'),
    path(r'<int:project_pk>/questionnaire/', include(question_patterns)),
    path(r'<int:project_pk>/donation-blueprints/', include(blueprint_patterns)),
    path(r'<int:project_pk>/exceptions/', project_admin.ExceptionList.as_view(), name='project-exceptions'),
]

authentication_patterns = [
    path(r'login/', project_admin.DdmLoginView.as_view(), name='ddm-login'),
    path(r'logout/', project_admin.DdmLogoutView.as_view(), name='ddm-logout'),
    path(r'register/', project_admin.DdmRegisterResearchProfileView.as_view(), name='ddm-register'),
    path(r'create-user/', project_admin.DdmCreateUserView.as_view(), name='ddm-create-user'),
    path(r'no-permission/', project_admin.DdmNoPermissionView.as_view(), name='ddm-no-permission'),
]

profile_patterns = [
    path(r'', project_admin.ProfileDetailView.as_view(), name='ddm-profile-detail'),
    path(r'change-password/', project_admin.ProfileChangePasswordView.as_view(), name='ddm-change-pw'),
    path(r'password-changed/', project_admin.ProfilePasswordChangedView.as_view(), name='ddm-pw-changed'),
]

urlpatterns = [
    path(r'<slug:slug>/', include(participation_flow_patterns)),
    path(r'projects/', include(project_admin_patterns)),
    path(r'auth/', include(authentication_patterns)),
    path(r'profile/', include(profile_patterns)),
    path(r'<int:pk>/download/', DownloadProjectDataView.as_view(), name='ddm-download-api'),
    path(r'<int:pk>/exceptions', ExceptionAPI.as_view(), name='ddm-exceptions-api'),
]
