#!/usr/bin/env python3
"""
🎵 Terminal Wrapped 2025 🎵
Your year in commands. The drama. The chaos. The mass-deleted node_modules.
"""

import os
import re
import time
import sys
from collections import Counter
from pathlib import Path

# ANSI color codes
class C:
    PINK = '\033[38;5;205m'
    GREEN = '\033[38;5;156m'
    BLUE = '\033[38;5;111m'
    ORANGE = '\033[38;5;216m'
    PURPLE = '\033[38;5;183m'
    YELLOW = '\033[38;5;229m'
    CYAN = '\033[38;5;123m'
    WHITE = '\033[38;5;255m'
    DIM = '\033[2m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def dramatic_pause(duration=0.8):
    time.sleep(duration)

def slow_print(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def press_enter():
    input(f"\n{C.DIM}  [ press enter to continue ]{C.RESET}")

def find_history_file():
    """Find the best history file."""
    home = Path.home()
    candidates = [
        (home / ".zsh_history", "zsh"),
        (home / ".bash_history", "bash"),
        (home / ".local/share/fish/fish_history", "fish"),
    ]
    
    for path, shell in candidates:
        if path.exists() and path.stat().st_size > 0:
            return path, shell
    return None, None

def parse_history(path, shell):
    """Parse history based on shell type."""
    commands = []
    with open(path, 'r', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if shell == "zsh":
                if line.startswith(':'):
                    match = re.match(r'^:\s*\d+:\d+;(.*)$', line)
                    if match:
                        commands.append(match.group(1))
                elif line and not line.startswith('#'):
                    commands.append(line)
            elif shell == "fish":
                if line.startswith('- cmd:'):
                    commands.append(line[6:].strip())
            else:  # bash
                if line and not line.startswith('#'):
                    commands.append(line)
    return commands

def get_base_command(cmd):
    """Extract base command, handling sudo/env/etc."""
    prefixes = ['sudo', 'time', 'nice', 'nohup', 'env', 'command', 'caffeinate']
    parts = cmd.split()
    while parts and parts[0] in prefixes:
        parts = parts[1:]
    if not parts:
        return cmd.split()[0] if cmd.split() else ''
    base = parts[0]
    if '/' in base:
        base = base.split('/')[-1]
    return base

def analyze(commands):
    """Extract all the juicy insights."""
    data = {}
    data['total'] = len(commands)
    
    # Base commands
    bases = [get_base_command(c) for c in commands if get_base_command(c)]
    data['top_commands'] = Counter(bases).most_common(15)
    data['unique_commands'] = len(set(bases))
    
    # Git deep dive
    git_cmds = [c for c in commands if c.startswith('git ')]
    if git_cmds:
        git_subs = [c.split()[1] for c in git_cmds if len(c.split()) > 1]
        data['git'] = {
            'total': len(git_cmds),
            'top': Counter(git_subs).most_common(5),
            'commits': git_subs.count('commit'),
            'pushes': git_subs.count('push'),
            'pulls': git_subs.count('pull'),
        }
    
    # Frustration indicators
    data['sudo_count'] = sum(1 for c in commands if c.startswith('sudo '))
    data['rm_rf_count'] = sum(1 for c in commands if 'rm -rf' in c or 'rm -r' in c)
    data['kill_count'] = sum(1 for c in commands if c.startswith(('kill ', 'killall ', 'pkill ')))
    
    # Package manager chaos
    data['npm_installs'] = sum(1 for c in commands if 'npm install' in c or 'npm i ' in c)
    data['pip_installs'] = sum(1 for c in commands if 'pip install' in c or 'pip3 install' in c)
    data['brew_installs'] = sum(1 for c in commands if 'brew install' in c)
    
    # Docker
    docker_cmds = [c for c in commands if c.startswith(('docker ', 'docker-compose ', 'docker compose '))]
    if docker_cmds:
        data['docker_total'] = len(docker_cmds)
    
    # SSH connections
    ssh_cmds = [c for c in commands if c.startswith('ssh ')]
    if ssh_cmds:
        data['ssh_count'] = len(ssh_cmds)
    
    # Repeated commands (doing the same thing over and over)
    cmd_counts = Counter(commands)
    most_repeated = cmd_counts.most_common(1)
    if most_repeated and most_repeated[0][1] > 5:
        data['most_repeated'] = most_repeated[0]
    
    # Typos/corrections
    typo_indicators = ['sl', 'gti', 'pyhton', 'pytho', 'ndoe', 'claer', 'clera', 'cd..', 'ls-la']
    data['typos'] = sum(1 for c in commands if any(c.startswith(t) or c == t for t in typo_indicators))
    
    # Late night commands (if zsh with timestamps)
    # We'd need timestamps for this, skipping for now
    
    # Navigation
    cd_cmds = [c for c in commands if c.startswith('cd ')]
    if cd_cmds:
        data['cd_count'] = len(cd_cmds)
    
    # Clear screen addiction
    data['clear_count'] = sum(1 for c in commands if c in ['clear', 'cls', 'reset'])
    
    # Vim vs others
    data['vim_opens'] = sum(1 for c in commands if c.startswith(('vim ', 'nvim ', 'vi ')))
    data['nano_opens'] = sum(1 for c in commands if c.startswith('nano '))
    data['code_opens'] = sum(1 for c in commands if c.startswith(('code ', 'code.')))
    
    # Cat abuse
    data['cat_count'] = sum(1 for c in commands if c.startswith('cat '))
    
    # Grep warrior
    data['grep_count'] = sum(1 for c in commands if 'grep' in c)
    
    # Find usage
    data['find_count'] = sum(1 for c in commands if c.startswith('find '))
    
    # Curl/wget
    data['curl_count'] = sum(1 for c in commands if c.startswith(('curl ', 'wget ')))
    
    # AWS
    data['aws_count'] = sum(1 for c in commands if c.startswith('aws '))
    
    # Kubectl
    data['kubectl_count'] = sum(1 for c in commands if c.startswith(('kubectl ', 'k ')) or c == 'k')
    
    return data

def print_title_card():
    clear_screen()
    print()
    print(f"{C.PINK}")
    print("  ╔════════════════════════════════════════════════════════════╗")
    print("  ║                                                            ║")
    print("  ║   ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ║")
    print("  ║   ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗║")
    print("  ║      ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║║")
    print("  ║      ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║║")
    print("  ║      ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║║")
    print("  ║      ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝║")
    print("  ║                                                            ║")
    print(f"  ║          {C.GREEN}W R A P P E D   2 0 2 5{C.PINK}                         ║")
    print("  ║                                                            ║")
    print("  ╚════════════════════════════════════════════════════════════╝")
    print(f"{C.RESET}")
    print()
    print(f"{C.DIM}           Your year in the terminal. No skips.{C.RESET}")
    print()

def show_total_commands(data):
    clear_screen()
    print()
    print()
    print()
    print(f"{C.DIM}  This year, you typed...{C.RESET}")
    dramatic_pause(1.5)
    print()
    print()
    print(f"{C.PINK}{C.BOLD}              {data['total']:,}{C.RESET}")
    print()
    print(f"{C.WHITE}              commands{C.RESET}")
    print()
    print()
    if data['total'] > 50000:
        print(f"{C.DIM}  That's... a lot. Are you okay?{C.RESET}")
    elif data['total'] > 20000:
        print(f"{C.DIM}  A power user. We see you.{C.RESET}")
    elif data['total'] > 5000:
        print(f"{C.DIM}  Solid. Consistent. Dedicated.{C.RESET}")
    else:
        print(f"{C.DIM}  Quality over quantity, right?{C.RESET}")

def show_top_command(data):
    clear_screen()
    print()
    print()
    if data['top_commands']:
        top_cmd, top_count = data['top_commands'][0]
        percentage = (top_count / data['total']) * 100
        
        print(f"{C.DIM}  Your #1 command was...{C.RESET}")
        dramatic_pause(1.5)
        print()
        print()
        print(f"{C.GREEN}{C.BOLD}              {top_cmd}{C.RESET}")
        print()
        print(f"{C.WHITE}              used {top_count:,} times ({percentage:.1f}% of all commands){C.RESET}")
        print()
        print()
        
        # Sassy commentary
        comments = {
            'ls': "You love to look around. Trust issues with your filesystem?",
            'cd': "Always on the move. Can't stay in one place.",
            'git': "Version control royalty. Your commits tell a story.",
            'vim': "A person of culture. Escape key worn smooth.",
            'nvim': "Neovim? Someone's got plugins to maintain.",
            'cat': "Just concatenating files, or using cat for everything?",
            'grep': "Searching for meaning in a sea of text.",
            'docker': "Containers. Containers everywhere.",
            'python': "Snake charmer energy.",
            'python3': "The explicit versioner. Respect.",
            'npm': "node_modules go brrrrr",
            'code': "VS Code truther. Valid.",
            'ssh': "Remote warrior. Touching grass? Never heard of it.",
            'make': "Building things the old-fashioned way.",
            'cargo': "Rustacean detected. Memory safety enthusiast.",
            'kubectl': "Kubernetes whisperer. How many clusters?",
            'aws': "Cloud native. Jeff Bezos thanks you.",
            'clear': "Clean terminal, clean mind. (Or hiding something?)",
        }
        if top_cmd in comments:
            print(f"{C.DIM}  {comments[top_cmd]}{C.RESET}")
        else:
            print(f"{C.DIM}  A classic. You know what you like.{C.RESET}")

def show_top_five(data):
    clear_screen()
    print()
    print(f"{C.PURPLE}  ┌─────────────────────────────────────┐{C.RESET}")
    print(f"{C.PURPLE}  │   {C.BOLD}YOUR TOP 5 COMMANDS{C.PURPLE}              │{C.RESET}")
    print(f"{C.PURPLE}  └─────────────────────────────────────┘{C.RESET}")
    print()
    
    medals = ['🥇', '🥈', '🥉', '4.', '5.']
    colors = [C.YELLOW, C.WHITE, C.ORANGE, C.DIM, C.DIM]
    
    for i, (cmd, count) in enumerate(data['top_commands'][:5]):
        dramatic_pause(0.4)
        bar_len = int((count / data['top_commands'][0][1]) * 20)
        bar = '█' * bar_len + '░' * (20 - bar_len)
        print(f"  {medals[i]} {colors[i]}{cmd:12}{C.CYAN} {bar} {C.WHITE}{count:,}{C.RESET}")
    print()

def show_git_stats(data):
    if 'git' not in data:
        return
    clear_screen()
    print()
    print(f"{C.ORANGE}  ┌─────────────────────────────────────┐{C.RESET}")
    print(f"{C.ORANGE}  │   {C.BOLD}YOUR GIT WRAPPED{C.ORANGE}                  │{C.RESET}")
    print(f"{C.ORANGE}  └─────────────────────────────────────┘{C.RESET}")
    print()
    
    g = data['git']
    print(f"  {C.WHITE}Total git commands:{C.GREEN} {g['total']:,}{C.RESET}")
    dramatic_pause(0.5)
    print(f"  {C.WHITE}Commits:{C.GREEN} {g['commits']:,}{C.RESET}")
    dramatic_pause(0.3)
    print(f"  {C.WHITE}Pushes:{C.GREEN} {g['pushes']:,}{C.RESET}")
    dramatic_pause(0.3)
    print(f"  {C.WHITE}Pulls:{C.GREEN} {g['pulls']:,}{C.RESET}")
    print()
    
    if g['commits'] > 0 and g['pushes'] > 0:
        ratio = g['commits'] / g['pushes']
        if ratio > 5:
            print(f"{C.DIM}  You commit way more than you push.{C.RESET}")
            print(f"{C.DIM}  Perfectionist? Or just scared of CI?{C.RESET}")
        elif ratio < 1.5:
            print(f"{C.DIM}  Push early, push often. YOLO deployment.{C.RESET}")
    
    if g['top']:
        print()
        print(f"  {C.DIM}Top git subcommands:{C.RESET}")
        for cmd, count in g['top'][:3]:
            print(f"    {C.CYAN}git {cmd}{C.WHITE} × {count}{C.RESET}")

def show_chaos_stats(data):
    clear_screen()
    print()
    print(f"{C.PINK}  ┌─────────────────────────────────────┐{C.RESET}")
    print(f"{C.PINK}  │   {C.BOLD}MOMENTS OF CHAOS{C.PINK}                  │{C.RESET}")
    print(f"{C.PINK}  └─────────────────────────────────────┘{C.RESET}")
    print()
    
    shown_something = False
    
    if data['sudo_count'] > 0:
        shown_something = True
        print(f"  {C.WHITE}Times you needed {C.ORANGE}sudo{C.WHITE}:{C.GREEN} {data['sudo_count']:,}{C.RESET}")
        if data['sudo_count'] > 500:
            print(f"  {C.DIM}  ^ Living dangerously. Root access enjoyer.{C.RESET}")
        dramatic_pause(0.4)
    
    if data['rm_rf_count'] > 0:
        shown_something = True
        print(f"  {C.WHITE}Times you ran {C.ORANGE}rm -rf{C.WHITE}:{C.GREEN} {data['rm_rf_count']:,}{C.RESET}")
        if data['rm_rf_count'] > 100:
            print(f"  {C.DIM}  ^ Deleting with confidence. Backups? Maybe.{C.RESET}")
        dramatic_pause(0.4)
    
    if data['kill_count'] > 0:
        shown_something = True
        print(f"  {C.WHITE}Processes {C.ORANGE}killed{C.WHITE}:{C.GREEN} {data['kill_count']:,}{C.RESET}")
        if data['kill_count'] > 50:
            print(f"  {C.DIM}  ^ Process assassin. No mercy.{C.RESET}")
        dramatic_pause(0.4)
    
    if data.get('clear_count', 0) > 100:
        shown_something = True
        print(f"  {C.WHITE}Screen {C.ORANGE}clears{C.WHITE}:{C.GREEN} {data['clear_count']:,}{C.RESET}")
        print(f"  {C.DIM}  ^ ctrl+l truther or compulsive clearer?{C.RESET}")
        dramatic_pause(0.4)
    
    if data.get('typos', 0) > 0:
        shown_something = True
        print(f"  {C.WHITE}Obvious {C.ORANGE}typos{C.WHITE} caught:{C.GREEN} {data['typos']:,}{C.RESET}")
        print(f"  {C.DIM}  ^ 'sl' and 'gti' send their regards.{C.RESET}")
    
    if not shown_something:
        print(f"  {C.DIM}  Surprisingly calm. No chaos detected.{C.RESET}")
        print(f"  {C.DIM}  (Are you even a developer?){C.RESET}")

def show_editor_war(data):
    vim = data.get('vim_opens', 0)
    nano = data.get('nano_opens', 0)
    code = data.get('code_opens', 0)
    
    if vim + nano + code < 10:
        return
    
    clear_screen()
    print()
    print(f"{C.BLUE}  ┌─────────────────────────────────────┐{C.RESET}")
    print(f"{C.BLUE}  │   {C.BOLD}EDITOR WARS: YOUR SIDE{C.BLUE}            │{C.RESET}")
    print(f"{C.BLUE}  └─────────────────────────────────────┘{C.RESET}")
    print()
    
    editors = [('vim/nvim', vim), ('VS Code', code), ('nano', nano)]
    editors.sort(key=lambda x: x[1], reverse=True)
    
    if editors[0][1] > 0:
        winner = editors[0][0]
        count = editors[0][1]
        print(f"  {C.WHITE}Your weapon of choice:{C.RESET}")
        dramatic_pause(0.8)
        print()
        print(f"  {C.GREEN}{C.BOLD}  {winner}{C.RESET}")
        print(f"  {C.DIM}  opened {count:,} times{C.RESET}")
        print()
        
        if 'vim' in winner.lower():
            print(f"  {C.DIM}  Modal editing supremacy. :wq gang.{C.RESET}")
        elif 'code' in winner.lower():
            print(f"  {C.DIM}  Extensions. Themes. The whole ecosystem.{C.RESET}")
        elif 'nano' in winner.lower():
            print(f"  {C.DIM}  Simple. Clean. No shame in that game.{C.RESET}")

def show_package_manager_chaos(data):
    npm = data.get('npm_installs', 0)
    pip = data.get('pip_installs', 0)
    brew = data.get('brew_installs', 0)
    
    if npm + pip + brew < 5:
        return
    
    clear_screen()
    print()
    print(f"{C.CYAN}  ┌─────────────────────────────────────┐{C.RESET}")
    print(f"{C.CYAN}  │   {C.BOLD}DEPENDENCY INSTALLATION THERAPY{C.CYAN}   │{C.RESET}")
    print(f"{C.CYAN}  └─────────────────────────────────────┘{C.RESET}")
    print()
    
    if npm > 0:
        print(f"  {C.WHITE}npm installs:{C.GREEN} {npm:,}{C.RESET}")
        if npm > 200:
            print(f"  {C.DIM}  ^ node_modules: the black hole of disk space{C.RESET}")
        dramatic_pause(0.4)
    
    if pip > 0:
        print(f"  {C.WHITE}pip installs:{C.GREEN} {pip:,}{C.RESET}")
        if pip > 100:
            print(f"  {C.DIM}  ^ requirements.txt keeps growing...{C.RESET}")
        dramatic_pause(0.4)
    
    if brew > 0:
        print(f"  {C.WHITE}brew installs:{C.GREEN} {brew:,}{C.RESET}")
        if brew > 50:
            print(f"  {C.DIM}  ^ Homebrew: because compiling is for suckers{C.RESET}")

def show_personality(data):
    clear_screen()
    print()
    print(f"{C.PURPLE}  ┌─────────────────────────────────────┐{C.RESET}")
    print(f"{C.PURPLE}  │   {C.BOLD}YOUR TERMINAL PERSONALITY{C.PURPLE}         │{C.RESET}")
    print(f"{C.PURPLE}  └─────────────────────────────────────┘{C.RESET}")
    print()
    dramatic_pause(1)
    
    # Determine personality based on patterns
    personalities = []
    
    if data.get('git', {}).get('total', 0) > data['total'] * 0.15:
        personalities.append("The Version Controller")
    if data.get('docker_total', 0) > 200:
        personalities.append("The Container Whisperer")
    if data.get('ssh_count', 0) > 100:
        personalities.append("The Remote Operator")
    if data.get('kubectl_count', 0) > 50:
        personalities.append("The Kubernetes Wrangler")
    if data.get('aws_count', 0) > 100:
        personalities.append("The Cloud Native")
    if data.get('grep_count', 0) > 500:
        personalities.append("The Pattern Matcher")
    if data.get('vim_opens', 0) > 200:
        personalities.append("The Modal Purist")
    if data.get('sudo_count', 0) > data['total'] * 0.1:
        personalities.append("The Superuser")
    if data.get('clear_count', 0) > 500:
        personalities.append("The Clean Freak")
    if data.get('rm_rf_count', 0) > 100:
        personalities.append("The Fearless Deleter")
    if data.get('curl_count', 0) > 100:
        personalities.append("The API Caller")
    if data.get('cat_count', 0) > 300:
        personalities.append("The File Peeker")
    
    if not personalities:
        personalities = ["The Generalist"]
    
    # Pick top personality
    personality = personalities[0]
    
    print(f"  {C.DIM}Based on your commands, you are...{C.RESET}")
    dramatic_pause(1.5)
    print()
    print(f"  {C.GREEN}{C.BOLD}  ✨ {personality} ✨{C.RESET}")
    print()
    
    # Sub-traits
    if len(personalities) > 1:
        print(f"  {C.DIM}With hints of:{C.RESET}")
        for p in personalities[1:4]:
            print(f"  {C.DIM}  • {p}{C.RESET}")

def show_most_repeated(data):
    if 'most_repeated' not in data:
        return
    
    cmd, count = data['most_repeated']
    if count < 20:
        return
    
    clear_screen()
    print()
    print(f"{C.ORANGE}  ┌─────────────────────────────────────┐{C.RESET}")
    print(f"{C.ORANGE}  │   {C.BOLD}YOUR MOST REPEATED COMMAND{C.ORANGE}        │{C.RESET}")
    print(f"{C.ORANGE}  └─────────────────────────────────────┘{C.RESET}")
    print()
    
    print(f"  {C.DIM}You typed this exact command {C.WHITE}{count}{C.DIM} times:{C.RESET}")
    dramatic_pause(1)
    print()
    
    # Truncate if too long
    display_cmd = cmd if len(cmd) < 50 else cmd[:47] + "..."
    print(f"  {C.GREEN}  {display_cmd}{C.RESET}")
    print()
    
    if count > 100:
        print(f"  {C.DIM}  Ever heard of shell aliases?{C.RESET}")
    elif count > 50:
        print(f"  {C.DIM}  Muscle memory is real.{C.RESET}")
    else:
        print(f"  {C.DIM}  A favorite command. We all have them.{C.RESET}")

def show_finale(data):
    clear_screen()
    print()
    print()
    print(f"{C.PINK}  ╔════════════════════════════════════════════════════════════╗{C.RESET}")
    print(f"{C.PINK}  ║                                                            ║{C.RESET}")
    print(f"{C.PINK}  ║  {C.WHITE}{C.BOLD}Thanks for a great year in the terminal.{C.PINK}                ║{C.RESET}")
    print(f"{C.PINK}  ║                                                            ║{C.RESET}")
    print(f"{C.PINK}  ║  {C.DIM}Here's to more commits, fewer bugs,{C.PINK}                    ║{C.RESET}")
    print(f"{C.PINK}  ║  {C.DIM}and maybe finally learning Vim properly.{C.PINK}                ║{C.RESET}")
    print(f"{C.PINK}  ║                                                            ║{C.RESET}")
    print(f"{C.PINK}  ╚════════════════════════════════════════════════════════════╝{C.RESET}")
    print()
    print()
    print(f"  {C.DIM}📊 Stats: {data['total']:,} commands | {data['unique_commands']:,} unique{C.RESET}")
    print()
    print(f"  {C.PURPLE}  #TerminalWrapped2025{C.RESET}")
    print()
    print()

def main():
    # Find history
    history_path, shell = find_history_file()
    
    if not history_path:
        print(f"{C.PINK}No shell history found!{C.RESET}")
        print("Looked for: ~/.zsh_history, ~/.bash_history, fish history")
        return
    
    # Parse it
    commands = parse_history(history_path, shell)
    
    if len(commands) < 50:
        print(f"{C.PINK}Not enough history to wrap!{C.RESET}")
        print(f"Only found {len(commands)} commands in {history_path}")
        return
    
    # Analyze
    data = analyze(commands)
    
    # The show begins
    print_title_card()
    press_enter()
    
    show_total_commands(data)
    press_enter()
    
    show_top_command(data)
    press_enter()
    
    show_top_five(data)
    press_enter()
    
    if 'git' in data:
        show_git_stats(data)
        press_enter()
    
    show_editor_war(data)
    press_enter()
    
    show_package_manager_chaos(data)
    press_enter()
    
    show_chaos_stats(data)
    press_enter()
    
    show_most_repeated(data)
    press_enter()
    
    show_personality(data)
    press_enter()
    
    show_finale(data)

if __name__ == "__main__":
    main()