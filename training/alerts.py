import resend
from .config import Config

def check_and_alert(rmse_cv, prev_rmse):
    if not Config.RESEND_API_KEY:
        print("No Resend API Key found. Skipping alerts.")
        return

    resend.api_key = Config.RESEND_API_KEY

    if prev_rmse is None:
        print("First run: No previous RMSE to compare.")
        return
    
    limit = prev_rmse * Config.FACTOR 

    if rmse_cv >= limit:
        print(f"Performance degraded! Current: {rmse_cv:.3f}, Limit: {limit:.3f}")
        
        params = {
            "from": "onboarding@resend.dev",
            "to": ["namann.parashar@gmail.com"], 
            "subject": "🚨 Model Alert: RMSE Degraded",
            "html": f"""
            <p><strong>Warning:</strong> The new model performance has dropped.</p>
            <ul>
                <li><strong>Previous RMSE:</strong> {prev_rmse:.3f}</li>
                <li><strong>Current RMSE:</strong> {rmse_cv:.3f}</li>
                <li><strong>Degradation:</strong> {((rmse_cv - prev_rmse)/prev_rmse)*100:.2f}% worse</li>
            </ul>
            """
        }
        try:
            resend.Emails.send(params)
            print("Alert email sent successfully.")
        except Exception as e:
            print(f"Failed to send email: {e}")
    else:
        print("Model performance is stable.")