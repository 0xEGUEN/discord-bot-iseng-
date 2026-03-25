#!/usr/bin/env node

/**
 * Discord Bot - Node.js Wrapper
 * Menjalankan Python bot.py dari Node.js
 */

import { spawn } from 'child_process';
import { existsSync } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load environment variables
dotenv.config();

// Helper function untuk log dengan prefix
const log = {
  info: (msg) => console.log(`\x1b[36m[INFO]\x1b[0m ${msg}`),
  success: (msg) => console.log(`\x1b[32m[SUCCESS]\x1b[0m ${msg}`),
  error: (msg) => console.log(`\x1b[31m[ERROR]\x1b[0m ${msg}`),
  warning: (msg) => console.log(`\x1b[33m[WARNING]\x1b[0m ${msg}`),
};

// Cek .env file
const envFile = path.join(__dirname, '.env');
if (!existsSync(envFile)) {
  log.error('.env file not found!');
  log.info('Please create .env file with DISCORD_TOKEN');
  process.exit(1);
}

// Cek Python installation
function checkPython() {
  return new Promise((resolve) => {
    const python = spawn('python', ['--version'], {
      stdio: 'pipe',
      shell: true
    });

    let pythonVersion = '';
    python.stdout.on('data', (data) => {
      pythonVersion += data.toString();
    });
    python.stderr.on('data', (data) => {
      pythonVersion += data.toString();
    });

    python.on('close', (code) => {
      if (code === 0) {
        resolve(pythonVersion.trim());
      } else {
        resolve(null);
      }
    });
  });
}

// Cek requirements.txt
function checkRequirements() {
  const reqFile = path.join(__dirname, 'requirements.txt');
  if (!existsSync(reqFile)) {
    log.error('requirements.txt not found!');
    log.info('Please ensure requirements.txt exists in the project directory');
    return false;
  }
  return true;
}

// Install Python dependencies
function installPythonDeps() {
  return new Promise((resolve) => {
    log.info('Installing Python dependencies...');
    const pip = spawn('pip', ['install', '-r', 'requirements.txt'], {
      stdio: 'inherit',
      shell: true,
      cwd: __dirname
    });

    pip.on('close', (code) => {
      if (code === 0) {
        log.success('Python dependencies installed');
        resolve(true);
      } else {
        log.error('Failed to install Python dependencies');
        resolve(false);
      }
    });
  });
}

// Run bot
function runBot() {
  log.info('Starting Discord Bot...');
  log.info('=' + '='.repeat(58) + '=');

  const botProcess = spawn('python', ['bot.py'], {
    stdio: 'inherit',
    shell: true,
    cwd: __dirname,
    env: { ...process.env }
  });

  botProcess.on('close', (code) => {
    if (code !== 0) {
      log.error(`Bot exited with code ${code}`);
    }
    process.exit(code);
  });

  botProcess.on('error', (err) => {
    log.error(`Failed to start bot: ${err.message}`);
    process.exit(1);
  });

  // Handle graceful shutdown
  process.on('SIGINT', () => {
    log.warning('Shutting down bot...');
    botProcess.kill('SIGTERM');
  });

  process.on('SIGTERM', () => {
    log.warning('Shutting down bot...');
    botProcess.kill('SIGTERM');
  });
}

// Main startup sequence
async function main() {
  try {
    console.log('\x1b[35m' + '='.repeat(60) + '\x1b[0m');
    console.log('\x1b[35m' + '    DISCORD BOT - NODE.JS WRAPPER' + '\x1b[0m');
    console.log('\x1b[35m' + '='.repeat(60) + '\x1b[0m\n');

    // Cek Python
    log.info('Checking Python installation...');
    const pythonVersion = await checkPython();
    
    if (!pythonVersion) {
      log.error('Python is not installed or not in PATH');
      log.info('Please install Python 3.10+ from https://www.python.org/');
      process.exit(1);
    }
    log.success(`Python found: ${pythonVersion}`);

    // Cek requirements
    if (!checkRequirements()) {
      process.exit(1);
    }
    log.success('requirements.txt found');

    // Install dependencies jika diperlukan
    const discordInstalled = await new Promise((resolve) => {
      const pythonCheck = spawn('python', ['-c', 'import discord'], {
        stdio: 'pipe',
        shell: true
      });
      pythonCheck.on('close', (code) => {
        resolve(code === 0);
      });
    });

    if (!discordInstalled) {
      log.warning('Discord.py not installed, installing...');
      await installPythonDeps();
    } else {
      log.success('All dependencies are installed');
    }

    console.log();
    runBot();

  } catch (err) {
    log.error(`Setup failed: ${err.message}`);
    process.exit(1);
  }
}

// Run
main();
