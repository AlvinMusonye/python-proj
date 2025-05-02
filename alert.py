import smtplib
from email.message import EmailMessage
import yfinance as yf
import pandas as pd
import config

def fetch_prices(ticker: str) -> pd.Series:
    """Download recent close prices for a given ticker."""
    print(f"Fetching prices for {ticker}...")
    data = yf.download(ticker, period="1mo", interval="1d")
    return data["Close"]  

def compute_signal(prices: pd.Series) -> pd.Series:
    """Return a Boolean series where True indicates a bullish MA crossover."""
    short_ma = prices.rolling(config.SHORT_WINDOW).mean()
    long_ma = prices.rolling(config.LONG_WINDOW).mean()

    return (short_ma.shift(1) < long_ma.shift(1)) & (short_ma > long_ma)

def send_email(subject: str, body: str) -> None:
    """Send an email via SMTP with the given subject and body."""
    print("Preparing to send email...")
    msg = EmailMessage()
    msg["From"] = config.FROM_ADDR
    msg["To"] = ", ".join(config.TO_ADDRS)
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
        server.starttls()
        server.login(config.EMAIL_USER, config.EMAIL_PASS)
        server.send_message(msg)
    print("Email sent successfully!")

def main():
    print("Starting trend alert check...")
    alerts = []
    for ticker in config.TICKERS:
        prices = fetch_prices(ticker)
        signals = compute_signal(prices)
        

        if True:
            print(f"Forced trend detected for {ticker} (test mode)!")
            alerts.append(f" {ticker}: (TEST) bullish crossover detected!")

    if alerts:
        body = " Hello Trader,\n\n"
        body = "Created by Liltop"
        body += "Here are today's trend signals:\n\n"
        body += "\n".join(f"- {alert}" for alert in alerts)
        body += "\n\nStay sharp and happy trading!\nYour Trend Alert Bot "
        send_email(config.SUBJECT, body)
        body = "\n".join(alerts)
        send_email(config.SUBJECT, body)
        print("Alerts sent:")
        print(body)
    else:
        print("No new trend signals. 📭")

if __name__ == "__main__":
    main()
