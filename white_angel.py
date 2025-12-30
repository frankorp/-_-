#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WHITE ANGEL - OSINT Investigator v3.0
Python инструмент для поиска информации
GitHub: https://github.com/ваш-ник/white-angel
Лицензия: MIT
"""

import requests
import json
import socket
import re
import os
import sys
from datetime import datetime
from urllib.parse import quote
import argparse
from colorama import init, Fore, Style

# Инициализация colorama для цветного вывода
init(autoreset=True)

class WhiteAngel:
    """Основной класс OSINT инструмента"""
    
    def __init__(self):
        self.version = "3.0"
        self.author = "White Angel Team"
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results = []
        
        # Настройки
        self.timeout = 10
        self.user_agent = "WhiteAngel/3.0"
        
    def print_banner(self):
        """Вывод баннера программы"""
        banner = f"""
{Fore.CYAN}
╔══════════════════════════════════════════════════╗
║               WHITE ANGEL OSINT                  ║
║               Investigator v{self.version}               ║
║                                                  ║
║  Автономный инструмент для поиска информации     ║
║  GitHub: github.com/ваш-ник/white-angel          ║
╚══════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
        print(banner)
        print(f"{Fore.YELLOW}[Сессия: {self.session_id}] [Время: {datetime.now().strftime('%H:%M:%S')}]{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*50}{Style.RESET_ALL}")
    
    def check_ip(self, ip_address):
        """Проверка IP адреса"""
        print(f"{Fore.BLUE}[🔍] Проверка IP: {ip_address}{Style.RESET_ALL}")
        
        try:
            # Проверка через ip-api.com
            response = requests.get(f"http://ip-api.com/json/{ip_address}", 
                                  timeout=self.timeout)
            data = response.json()
            
            if data['status'] == 'success':
                print(f"{Fore.GREEN}[+] Страна: {data.get('country', 'N/A')}")
                print(f"[+] Город: {data.get('city', 'N/A')}")
                print(f"[+] Регион: {data.get('regionName', 'N/A')}")
                print(f"[+] Провайдер: {data.get('isp', 'N/A')}")
                print(f"[+] Координаты: {data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}")
                print(f"[+] Часовой пояс: {data.get('timezone', 'N/A')}{Style.RESET_ALL}")
                
                # Сохраняем результат
                self.results.append({
                    'type': 'ip',
                    'target': ip_address,
                    'data': data,
                    'timestamp': datetime.now().isoformat()
                })
                
                return data
            else:
                print(f"{Fore.RED}[-] Ошибка при проверке IP{Style.RESET_ALL}")
                return None
                
        except Exception as e:
            print(f"{Fore.RED}[-] Ошибка: {str(e)}{Style.RESET_ALL}")
            return None
    
    def check_phone(self, phone_number):
        """Проверка телефонного номера"""
        print(f"{Fore.BLUE}[📱] Проверка телефона: {phone_number}{Style.RESET_ALL}")
        
        # Очистка номера
        clean_phone = re.sub(r'[^0-9+]', '', phone_number)
        
        print(f"{Fore.GREEN}[+] Очищенный номер: {clean_phone}")
        
        # Определение страны по префиксу
        country_info = self._detect_country(clean_phone)
        print(f"[+] Страна: {country_info.get('country', 'Неизвестно')}")
        
        # Ссылки на мессенджеры
        print(f"{Fore.GREEN}[+] Мессенджеры:{Style.RESET_ALL}")
        print(f"    WhatsApp: https://wa.me/{clean_phone}")
        print(f"    Telegram: https://t.me/{clean_phone}")
        
        # Поиск в соцсетях
        print(f"{Fore.GREEN}[+] Поиск в соцсетях:{Style.RESET_ALL}")
        print(f"    ВКонтакте: https://vk.com/phone/{clean_phone}")
        
        # Поиск в Google
        search_query = quote(f'"{phone_number}" OR "{clean_phone}"')
        print(f"{Fore.GREEN}[+] Поиск в интернете:{Style.RESET_ALL}")
        print(f"    Google: https://www.google.com/search?q={search_query}")
        
        # Сохраняем результат
        self.results.append({
            'type': 'phone',
            'target': phone_number,
            'clean': clean_phone,
            'country': country_info,
            'timestamp': datetime.now().isoformat()
        })
        
        return {
            'clean_phone': clean_phone,
            'country': country_info,
            'links': {
                'whatsapp': f'https://wa.me/{clean_phone}',
                'telegram': f'https://t.me/{clean_phone}',
                'vk': f'https://vk.com/phone/{clean_phone}'
            }
        }
    
    def check_email(self, email_address):
        """Проверка email адреса"""
        print(f"{Fore.BLUE}[📧] Проверка email: {email_address}{Style.RESET_ALL}")
        
        # Проверка формата
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email_address):
            print(f"{Fore.RED}[-] Неверный формат email{Style.RESET_ALL}")
            return None
        
        print(f"{Fore.GREEN}[+] Формат корректный{Style.RESET_ALL}")
        
        # Разделение email
        local_part, domain = email_address.split('@')
        print(f"{Fore.GREEN}[+] Локальная часть: {local_part}")
        print(f"[+] Домен: {domain}{Style.RESET_ALL}")
        
        # Проверка DNS
        try:
            socket.gethostbyname(domain)
            print(f"{Fore.GREEN}[+] Домен существует{Style.RESET_ALL}")
        except:
            print(f"{Fore.YELLOW}[-] Домен не найден{Style.RESET_ALL}")
        
        # Поиск в соцсетях
        print(f"{Fore.GREEN}[+] Поиск в соцсетях:{Style.RESET_ALL}")
        print(f"    ВКонтакте: https://vk.com/{local_part}")
        print(f"    Telegram: https://t.me/{local_part}")
        print(f"    GitHub: https://github.com/{local_part}")
        
        # Проверка утечек
        print(f"{Fore.GREEN}[+] Проверка утечек:{Style.RESET_ALL}")
        print(f"    Have I Been Pwned: https://haveibeenpwned.com/account/{email_address}")
        
        # Поиск в Google
        search_query = quote(f'"{email_address}" OR "{local_part}"')
        print(f"{Fore.GREEN}[+] Поиск в интернете:{Style.RESET_ALL}")
        print(f"    Google: https://www.google.com/search?q={search_query}")
        
        # Сохраняем результат
        self.results.append({
            'type': 'email',
            'target': email_address,
            'local_part': local_part,
            'domain': domain,
            'timestamp': datetime.now().isoformat()
        })
        
        return {
            'local_part': local_part,
            'domain': domain,
            'links': {
                'vk': f'https://vk.com/{local_part}',
                'telegram': f'https://t.me/{local_part}',
                'github': f'https://github.com/{local_part}'
            }
        }
    
    def search_username(self, username):
        """Поиск пользователя по никнейму"""
        print(f"{Fore.BLUE}[👤] Поиск никнейма: {username}{Style.RESET_ALL}")
        
        # Платформы для поиска
        platforms = [
            ('VK', f'https://vk.com/{username}'),
            ('Telegram', f'https://t.me/{username}'),
            ('GitHub', f'https://github.com/{username}'),
            ('Instagram', f'https://instagram.com/{username}'),
            ('Twitter/X', f'https://twitter.com/{username}'),
            ('YouTube', f'https://youtube.com/@{username}'),
            ('Steam', f'https://steamcommunity.com/id/{username}')
        ]
        
        found = []
        print(f"{Fore.YELLOW}[*] Проверяем платформы...{Style.RESET_ALL}")
        
        for platform_name, url in platforms:
            try:
                response = requests.head(url, timeout=5, allow_redirects=True)
                if response.status_code < 400:
                    found.append((platform_name, url))
                    print(f"{Fore.GREEN}    ✓ {platform_name}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.WHITE}    ✗ {platform_name}{Style.RESET_ALL}")
            except:
                print(f"{Fore.WHITE}    ? {platform_name}{Style.RESET_ALL}")
        
        if found:
            print(f"{Fore.GREEN}[+] Найдено профилей: {len(found)}{Style.RESET_ALL}")
            for platform_name, url in found:
                print(f"    • {platform_name}: {url}")
        else:
            print(f"{Fore.YELLOW}[-] Профили не найдены{Style.RESET_ALL}")
        
        # Поиск в Google
        search_query = quote(f'"{username}"')
        print(f"{Fore.GREEN}[+] Поиск в интернете:{Style.RESET_ALL}")
        print(f"    Google: https://www.google.com/search?q={search_query}")
        
        # Сохраняем результат
        self.results.append({
            'type': 'username',
            'target': username,
            'found_profiles': found,
            'timestamp': datetime.now().isoformat()
        })
        
        return {
            'username': username,
            'found_profiles': found
        }
    
    def save_report(self, filename=None):
        """Сохранение отчета"""
        if not self.results:
            print(f"{Fore.YELLOW}[-] Нет данных для сохранения{Style.RESET_ALL}")
            return None
        
        if not filename:
            filename = f"white_angel_report_{self.session_id}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'tool': 'White Angel OSINT',
                    'version': self.version,
                    'session_id': self.session_id,
                    'timestamp': datetime.now().isoformat(),
                    'results': self.results
                }, f, ensure_ascii=False, indent=2)
            
            print(f"{Fore.GREEN}[+] Отчет сохранен: {filename}{Style.RESET_ALL}")
            return filename
        except Exception as e:
            print(f"{Fore.RED}[-] Ошибка сохранения: {str(e)}{Style.RESET_ALL}")
            return None
    
    def _detect_country(self, phone):
        """Определение страны по номеру телефона"""
        phone = phone.replace('+', '')
        
        # Россия
        if phone.startswith('7'):
            return {
                'country': 'Россия 🇷🇺',
                'code': 'RU',
                'operators': ['МТС', 'Билайн', 'МегаФон', 'Теле2']
            }
        # Украина
        elif phone.startswith('380'):
            return {
                'country': 'Украина 🇺🇦',
                'code': 'UA',
                'operators': ['Киевстар', 'Vodafone', 'lifecell']
            }
        # Беларусь
        elif phone.startswith('375'):
            return {
                'country': 'Беларусь 🇧🇾',
                'code': 'BY',
                'operators': ['МТС', 'А1', 'life:)' ]
            }
        # Казахстан
        elif phone.startswith('7') and len(phone) == 11:
            return {
                'country': 'Казахстан 🇰🇿',
                'code': 'KZ',
                'operators': ['Beeline', 'Kcell', 'Tele2']
            }
        else:
            return {
                'country': 'Неизвестно',
                'code': 'XX',
                'operators': []
            }
    
    def run_interactive(self):
        """Интерактивный режим"""
        self.print_banner()
        
        while True:
            print(f"\n{Fore.CYAN}[ МЕНЮ ]{Style.RESET_ALL}")
            print("1. 🔍 Проверить IP адрес")
            print("2. 📱 Проверить телефон")
            print("3. 📧 Проверить email")
            print("4. 👤 Найти по никнейму")
            print("5. 💾 Сохранить отчет")
            print("6. 🚪 Выход")
            
            choice = input(f"\n{Fore.YELLOW}[?] Выберите действие (1-6): {Style.RESET_ALL}").strip()
            
            if choice == '1':
                ip = input(f"{Fore.BLUE}[IP] Введите IP адрес: {Style.RESET_ALL}").strip()
                if ip:
                    self.check_ip(ip)
            
            elif choice == '2':
                phone = input(f"{Fore.BLUE}[Phone] Введите телефон: {Style.RESET_ALL}").strip()
                if phone:
                    self.check_phone(phone)
            
            elif choice == '3':
                email = input(f"{Fore.BLUE}[Email] Введите email: {Style.RESET_ALL}").strip()
                if email:
                    self.check_email(email)
            
            elif choice == '4':
                username = input(f"{Fore.BLUE}[Username] Введите никнейм: {Style.RESET_ALL}").strip()
                if username:
                    self.search_username(username)
            
            elif choice == '5':
                self.save_report()
            
            elif choice == '6':
                print(f"\n{Fore.GREEN}[+] Спасибо за использование White Angel!{Style.RESET_ALL}")
                break
            
            else:
                print(f"\n{Fore.RED}[-] Неверный выбор{Style.RESET_ALL}")
            
            input(f"\n{Fore.WHITE}[Нажмите Enter чтобы продолжить...]{Style.RESET_ALL}")

def main():
    """Основная функция"""
    parser = argparse.ArgumentParser(description='White Angel OSINT Tool')
    parser.add_argument('--ip', help='Проверить IP адрес')
    parser.add_argument('--phone', help='Проверить телефон')
    parser.add_argument('--email', help='Проверить email')
    parser.add_argument('--username', help='Найти по никнейму')
    parser.add_argument('--save', help='Сохранить отчет в файл')
    parser.add_argument('--interactive', '-i', action='store_true', help='Интерактивный режим')
    
    args = parser.parse_args()
    
    # Создаем экземпляр инструмента
    tool = WhiteAngel()
    
    # Если есть аргументы - выполняем их
    if args.ip:
        tool.check_ip(args.ip)
    if args.phone:
        tool.check_phone(args.phone)
    if args.email:
        tool.check_email(args.email)
    if args.username:
        tool.search_username(args.username)
    
    # Сохраняем если нужно
    if args.save:
        tool.save_report(args.save)
    
    # Если нет аргументов или интерактивный режим
    if not any([args.ip, args.phone, args.email, args.username, args.save]) or args.interactive:
        tool.run_interactive()
    
    # Сохраняем автоматически если были проверки
    if tool.results and not args.save:
        tool.save_report()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Программа прервана{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[!] Критическая ошибка: {e}{Style.RESET_ALL}")
