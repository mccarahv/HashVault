import sys
import pandas as pd
import requests
import hashlib
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog,
                             QLabel, QMessageBox, QTabWidget, QLineEdit, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QHeaderView, QComboBox)
from web3 import Web3
import json
import os

class FileChooserApp(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Hash Vault'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.selected_file = ''
        self.file_type = ''
        self.file_hash = ''
        self.data_file = 'file_records.json'
        self.file_records = []

        self.initUI()
        self.loadFileRecords()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()

        self.tabs.addTab(self.tab1, "Select File")
        self.tabs.addTab(self.tab2, "Hash File")
        self.tabs.addTab(self.tab3, "Blockchain Interaction")
        self.tabs.addTab(self.tab4, "File Records")

        self.initTab1()
        self.initTab2()
        self.initTab3()
        self.initTab4()

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def initTab1(self):
        layout = QVBoxLayout()
        self.btnChooseFile = QPushButton('Choose File')
        self.btnChooseFile.clicked.connect(self.openFileNameDialog)
        layout.addWidget(self.btnChooseFile)
        self.selectedFileLabel = QLabel('File Name: None Selected')
        layout.addWidget(self.selectedFileLabel)
        self.fileTypeLabel = QLabel('File Type: NA')
        layout.addWidget(self.fileTypeLabel)
        self.statusLabelTab1 = QLabel('Status: Select File')
        layout.addWidget(self.statusLabelTab1)
        self.tab1.setLayout(layout)

    def initTab2(self):
        layout = QVBoxLayout()    
        self.btnHashFile = QPushButton('Hash File')
        self.btnHashFile.clicked.connect(self.hashFile)
        layout.addWidget(self.btnHashFile)  
        self.fileNameLabel = QLabel('File Name: None selected')
        layout.addWidget(self.fileNameLabel)    
        self.hashFileLabel = QLabel('File Hash: Not yet computed')
        layout.addWidget(self.hashFileLabel)    
        self.hashIDLabel = QLabel('Hash ID: Not assigned')
        layout.addWidget(self.hashIDLabel)    
        self.statusLabelTab2 = QLabel('Status: Awaiting hash computation')
        layout.addWidget(self.statusLabelTab2)      
        self.tab2.setLayout(layout)


    def initTab3(self):
        layout = QVBoxLayout()
        self.fileComboBox = QComboBox()
        self.fileComboBox.currentIndexChanged.connect(self.updateSelectedFileInfo)
        layout.addWidget(self.fileComboBox)
        self.btnSendToEthereum = QPushButton('Send Hash to Ethereum')
        self.btnSendToEthereum.clicked.connect(self.sendHashToEthereum)
        layout.addWidget(self.btnSendToEthereum)
        self.ethTransactionHashLabel = QLabel('Ethereum Transaction Hash Receipt: ')
        layout.addWidget(self.ethTransactionHashLabel)
        self.hashIDNumberLabel = QLabel('Hash ID Number: ')
        layout.addWidget(self.hashIDNumberLabel)
        self.storedFileHashLabel = QLabel("Your File's Stored Hash: ")
        layout.addWidget(self.storedFileHashLabel)
        self.tab3.setLayout(layout)

    def initTab4(self):
        layout = QVBoxLayout()
        self.fileTable = QTableWidget()
        self.fileTable.setColumnCount(4)
        self.fileTable.setHorizontalHeaderLabels(['File Name', 'File Hash', 'Hash ID Number', 'Ethereum Txn Receipt'])
        self.fileTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.fileTable)
        searchLayout = QHBoxLayout()
        self.searchInput = QLineEdit()
        self.searchInput.setPlaceholderText('Enter file name, hash ID, or file hash to find details')
        searchLayout.addWidget(self.searchInput)
        self.btnSearch = QPushButton('Search')
        self.btnSearch.clicked.connect(self.searchFileRecord)
        searchLayout.addWidget(self.btnSearch)
        layout.addLayout(searchLayout)
        self.btnClearData = QPushButton('Clear Data')
        self.btnClearData.clicked.connect(self.clearData)
        layout.addWidget(self.btnClearData)
        self.tab4.setLayout(layout)

    def updateBlockchainDropdown(self):
        self.fileComboBox.clear()
        current_data_index = -1
        for index, (fileName, fileHash, hashID, ethTxReceipt) in enumerate(self.file_records):
            if not ethTxReceipt:  
                self.fileComboBox.addItem(fileName, (fileName, fileHash, hashID, ethTxReceipt))
                if fileName == self.selected_file:
                    current_data_index = index
    
        if current_data_index != -1:
            self.fileComboBox.setCurrentIndex(current_data_index)


    def updateSelectedFileInfo(self):
        selected_data = self.fileComboBox.currentData()
        if selected_data:
            fileName, file_hash, hashID, ethTxReceipt = selected_data
            self.hashIDNumberLabel.setText(f'Hash ID: {hashID}')
            self.storedFileHashLabel.setText(f"Your File's Stored Hash: {file_hash}")
            self.ethTransactionHashLabel.setText(f"Ethereum Transaction Hash Receipt: {ethTxReceipt if ethTxReceipt else 'Not yet sent to blockchain'}")
        else:
            self.hashIDNumberLabel.setText('Hash ID Number: Not available')
            self.storedFileHashLabel.setText("Your File's Stored Hash: Not available")
            self.ethTransactionHashLabel.setText('Ethereum Transaction Hash Receipt: Not available')

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;CSV Files (*.csv);;Text Files (*.txt);;Excel Files (*.xlsx)",
                                                  options=options)
        if fileName:
            self.selected_file = fileName
            self.selectedFileLabel.setText(f'Selected file: {fileName.split('/')[-1]}')
            self.fileNameLabel.setText(f'File Name: {fileName.split('/')[-1]}')  # Update file name on Hash File tab immediately
            if fileName.lower().endswith('.csv') or fileName.lower().endswith('.xlsx') or fileName.lower().endswith('.txt'):
                self.file_type = fileName.split('.')[-1].upper()
                self.fileTypeLabel.setText(f'File Type: {self.file_type}')
                self.statusLabelTab1.setText('Status: Proceed to Hash File Tab')
                self.statusLabelTab2.setText('Status: Ready to hash')
            else:
                self.file_type = 'Unknown'
                self.fileTypeLabel.setText(f'File Type: {self.file_type}')
                self.statusLabelTab1.setText('Status: Unsupported file type')
                QMessageBox.warning(self, 'File Type Error', 'Unsupported file type selected. Only accepts: CSV, TXT, XLSX.')


    def hashFile(self):
        if not self.selected_file:
            QMessageBox.warning(self, 'File Not Selected', 'Please select a file first.')
            return
    
        file_name = self.selected_file.split('/')[-1]
        if any(file_name == record[0] for record in self.file_records):
            QMessageBox.warning(self, 'File Already Processed', 'This file has already been hashed.')
            return
    
        try:
            if self.file_type in ['CSV', 'XLSX', 'TXT']:
                # Read data based on the file type
                if self.file_type == 'CSV':
                    df = pd.read_csv(self.selected_file)
                elif self.file_type == 'XLSX':
                    df = pd.read_excel(self.selected_file)
                else:
                    with open(self.selected_file, 'r') as file:
                        data = file.read()
                    df = pd.DataFrame([data], columns=['Data'])
    
                file_hash = self.hash_dataframe(df)
                hash_id = len(self.file_records) + 1
    
                self.updateFileRecords(file_name, file_hash, hash_id, "")
                self.updateTable()
                self.updateBlockchainDropdown()
    
                self.fileComboBox.setCurrentIndex(self.fileComboBox.findText(file_name))
    
                self.hashFileLabel.setText(f'File Hash: {file_hash}')
                self.hashIDLabel.setText(f'Hash ID: {hash_id}')
                self.statusLabelTab2.setText('Status: Proceed to Blockchain Interaction Tab')
    
            else:
                self.hashFileLabel.setText('File Hash: Error - Unsupported file type')
                self.statusLabelTab2.setText('Status: Error due to unsupported file type')
        except Exception as e:
            QMessageBox.critical(self, "Hashing Error", "An error occurred while processing the file: " + str(e))
            self.statusLabelTab2.setText('Status: Error during hashing')

    def hash_dataframe(self, dataframe):
        df_string = dataframe.to_string(header=True, index=False)
        return hashlib.sha256(df_string.encode()).hexdigest()

    def updateFileRecords(self, fileName, fileHash, hashID, ethTxReceipt):
        # Ensuring that each record is a list
        self.file_records.append([fileName, fileHash, hashID, ethTxReceipt])
        self.updateTable()

    def updateTable(self):
        self.fileTable.setRowCount(len(self.file_records))
        for row, (fileName, fileHash, hashID, ethTxReceipt) in enumerate(self.file_records):
            self.fileTable.setItem(row, 0, QTableWidgetItem(fileName))
            self.fileTable.setItem(row, 1, QTableWidgetItem(fileHash))
            self.fileTable.setItem(row, 2, QTableWidgetItem(str(hashID)))
            self.fileTable.setItem(row, 3, QTableWidgetItem(ethTxReceipt))

    def clearData(self):
        reply = QMessageBox.question(self, 'Clear Data', 'Are you sure you want to clear all data?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.file_records.clear()
            self.updateTable()
            self.saveFileRecords()

    def sendHashToEthereum(self):
        selected_data = self.fileComboBox.currentData()
        if not selected_data:
            QMessageBox.warning(self, 'Selection Error', 'Please select a file to send to Ethereum.')
            return
        fileName, file_hash, hashID, _ = selected_data
        try:
            infura_api_key = "#####"
            sepolia_infura_url = f"https://sepolia.infura.io/v3/{infura_api_key}"
            w3 = Web3(Web3.HTTPProvider(sepolia_infura_url))
            assert w3.is_connected(), "Web3 is not connected to Ethereum network!"
            contract_address = "#####"
            with open('/Users/dev/Desktop/HashAI/build/contracts/HashStore.json') as f:
                contract_data = json.load(f)
                contract_abi = contract_data['abi']
            contract = w3.eth.contract(address=contract_address, abi=contract_abi)
            from_address = "####"
            private_key = "####"
            nonce = w3.eth.get_transaction_count(from_address)
            transaction = contract.functions.storeHash(file_hash).build_transaction({
                'chainId': 11155111,
                'gas': 2000000,
                'gasPrice': w3.to_wei('50', 'gwei'),
                'nonce': nonce,
                'from': from_address
            })
            signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            for record in self.file_records:
                if record[0] == fileName and record[1] == file_hash and record[2] == hashID:
                    record[3] = tx_hash.hex()
                    break
            self.updateTable()
            self.updateBlockchainDropdown()
            self.ethTransactionHashLabel.setText(f'Ethereum Transaction Hash Receipt: {tx_hash.hex()}')
            print(f'Transaction successful with hash: {tx_hash.hex()}')
        except Exception as e:
            QMessageBox.critical(self, 'Transaction Failed', str(e))

    def closeEvent(self, event):
        self.saveFileRecords()
        event.accept()

    def loadFileRecords(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                self.file_records = json.load(file)
            self.updateTable()
            self.updateBlockchainDropdown()
            if self.fileComboBox.count() > 0:
                self.updateSelectedFileInfo()

    def get_transaction_timestamp(self, tx_hash):
        if not tx_hash:
            return 'Not Published to Ethereum Yet'
        api_key = '####'
        url = f'https://api-sepolia.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={tx_hash}&apikey={api_key}'
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception('Failed to fetch data from Etherscan')
        transaction_details = response.json()
        if transaction_details['result']:
            block_number = transaction_details['result']['blockNumber']
            block_url = f'https://api-sepolia.etherscan.io/api?module=proxy&action=eth_getBlockByNumber&tag={block_number}&boolean=true&apikey={api_key}'
            block_response = requests.get(block_url)
            if block_response.status_code != 200:
                raise Exception('Failed to fetch block data from Etherscan')
            block_details = block_response.json()
            if block_details['result']:
                timestamp = int(block_details['result']['timestamp'], 16)
                from datetime import datetime
                timestamp = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M UTC')
                return timestamp
        return 'Timestamp not available'

    def searchFileRecord(self):
        search_text = self.searchInput.text().strip().lower()
        found_record = None
        for fileName, fileHash, hashID, ethTxReceipt in self.file_records:
            if search_text in [fileName.lower(), fileHash.lower(), str(hashID).lower()]:
                found_record = (fileName, fileHash, hashID, ethTxReceipt)
                break
    
        if found_record:
            txn_receipt = found_record[3] if found_record[3] else 'Not Published to Ethereum Yet'
            timestamp_msg = 'Not Published to Ethereum Yet'
            if found_record[3]:
                try:
                    timestamp_msg = self.get_transaction_timestamp(found_record[3])
                except Exception as e:
                    timestamp_msg = f'Failed to retrieve timestamp: {str(e)}'
            QMessageBox.information(self, 'Search Result', f"File Name: {found_record[0]}\n"
                                                           f"File Hash: {found_record[1]}\n"
                                                           f"Hash ID: {found_record[2]}\n"
                                                           f"Ethereum Txn Receipt: {txn_receipt}\n"
                                                           f"Transaction Timestamp: {timestamp_msg}")
        else:
            QMessageBox.warning(self, 'Search Result', 'No matching record found.')

    def saveFileRecords(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.file_records, file)

def main():
    app = QApplication(sys.argv)
    ex = FileChooserApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
