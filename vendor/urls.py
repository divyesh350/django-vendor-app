from django.urls import path
from vendor.views import SendOTPView, VerifyOTPView, SignupView, GetProfileView, UploadDocumentView, GetDocumentsView, GetDocumentView, WalletView, GenerateQuotationPDFView


app_name = 'vendor'

urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('profile/', GetProfileView.as_view(), name='profile'),
    path('upload-document/', UploadDocumentView.as_view(), name='upload_document'),
    path('documents/', GetDocumentsView.as_view(), name='documents'),
    path('documents/<int:document_id>/', GetDocumentView.as_view(), name='document_detail'),
    path('wallet/', WalletView.as_view(), name='wallet'),
    path('generate-quotation-pdf/', GenerateQuotationPDFView.as_view(), name='generate-quotation-pdf'),
]