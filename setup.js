#!/usr/bin/env node

/**
 * Setup Script - Automated Bot Setup
 * Guides user through initial setup
 */

import { spawn } from 'child_process';
import { existsSync, readFileSync, writeFileSync, copyFileSync } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import readline from 'readline';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const log = {
  info: (msg) => console.log(`\x1b[36m[INFO]\x1b[0m ${msg}`),
  success: (msg) => console.log(`\x1b[32m[✓]\x1b[0m ${msg}`),
  error: (msg) => console.log(`\x1b[31m[✗]\x1b[0m ${msg}`),
  warning: (msg) => console.log(`\x1b[33m[!]\x1b[0m ${msg}`),
};

function question(prompt) {
  return new Promise((resolve) => {
    rl.question(prompt, (answer) => {
      resolve(answer);
    });
  });
}

async function setup() {
  console.log('\n\x1b[35m' + '='.repeat(60) + '\x1b[0m');
  console.log('\x1b[35m' + '    DISCORD BOT SETUP' + '\x1b[0m');
  console.log('\x1b[35m' + '='.repeat(60) + '\x1b[0m\n');

  // Step 1: Check .env
  log.info('Step 1: Checking .env configuration...');
  const envPath = path.join(__dirname, '.env');
  const envExamplePath = path.join(__dirname, '.env.example');

  if (!existsSync(envPath)) {
    if (existsSync(envExamplePath)) {
      log.warning('.env not found. Creating from .env.example...');
      copyFileSync(envExamplePath, envPath);
      log.success('.env created');
    } else {
      log.warning('.env not found. Creating default...');
      writeFileSync(envPath, 'DISCORD_TOKEN=your_token_here\n');
      log.success('.env created');
    }
  } else {
    log.success('.env file exists');
  }

  // Step 2: Ask for Discord Token
  const setupToken = await question(
    '\nDo you want to add/update Discord Token? (y/n): '
  );

  if (setupToken.toLowerCase() === 'y') {
    const token = await question('Enter your Discord Bot Token: ');
    if (token && token.length > 0) {
      let envContent = '';
      if (existsSync(envPath)) {
        envContent = readFileSync(envPath, 'utf8');
      }

      if (envContent.includes('DISCORD_TOKEN=')) {
        envContent = envContent.replace(
          /DISCORD_TOKEN=.*/,
          `DISCORD_TOKEN=${token}`
        );
      } else {
        envContent += `DISCORD_TOKEN=${token}\n`;
      }

      writeFileSync(envPath, envContent);
      log.success('Discord Token saved');
    }
  }

  // Step 3: Install dependencies
  log.info('\nStep 2: Installing dependencies...');
  const installDeps = await question(
    'Install Python dependencies? (y/n): '
  );

  if (installDeps.toLowerCase() === 'y') {
    log.info('Installing Python dependencies...');
    await new Promise((resolve) => {
      const pip = spawn('pip', ['install', '-r', 'requirements.txt'], {
        stdio: 'inherit',
        shell: true,
        cwd: __dirname
      });

      pip.on('close', (code) => {
        if (code === 0) {
          log.success('Dependencies installed');
        } else {
          log.error('Failed to install dependencies');
        }
        resolve();
      });
    });
  }

  // Step 4: Summary
  console.log('\n\x1b[35m' + '='.repeat(60) + '\x1b[0m');
  console.log('\x1b[32m✓ Setup Complete!\x1b[0m\n');
  console.log('Next steps:');
  console.log('  1. Make sure DISCORD_TOKEN is set in .env');
  console.log('  2. Invite bot to your Discord server');
  console.log('  3. Run the bot:\n');
  console.log('     \x1b[36mnpm start\x1b[0m\n');
  console.log('\x1b[35m' + '='.repeat(60) + '\x1b[0m\n');

  rl.close();
}

setup();
