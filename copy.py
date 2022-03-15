import datetime
import hashlib
import json
from flask import Flask,jsonify,request
from weakref.wrappers import response

#structuring the blockchain
class blockchain:

     def__init__(self):
         self.chain = []
         self.create_block(owner='creator', reg_no='007',proof=1, previous_hash='0')

    def create_block(self,owner,reg_no,proof,previous_hash):
        block = { 'owner': owner,
                  'reg_no' : reg_no,
                  'index' :len(self.chain)+1,
                  'timestamp' :str(datetime.datetime.now()),
                  'proof':proof,
                  'previous_hash':previous_hash

        }
        self.chain.append(block)
        return block


    def proof_of_work(self, previous_proof):
        new_proof =1
        check_proof=False

        while check_proof is False:
            hash_val = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_val[:4]=='0000':
                check_proof=True
            else:
                new_proof+=1


        return new_proof  

    
    def hash(self,block):
        encooded_block = json.dumps(block).encode()
        return hashlib.sha256(encooded_block).hexdigest()
    


    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_idx = 1

        while block_idx <len(chain):
            block = chain[block_idx]
            if block['previous_hash'] != self.hash(previous_block):
                return False 
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_val = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_val[:4] != '0000':
                return False
            previous_block = block
            block_idx +=1

        return True 

    def get_last_block(self):
        return self.chain[-1]


#creating the web app

app = Flask(__name__)


blockchain = blockchain()

#getting full blockchain 
@app.route('/get_chain',method=['GET'])
def get_chain():
    response = {
        'chain':blockchain.chain,
        'length':len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/is_valid',methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)

    if is_valid:
        response = {'message': 'All good . the ledger is valid '}

    else:
      response ={'message': 'Sir, we have a problem. the record are not valid'}

    return jsonify(response), 200

@app.route('/mine_block' , methods=['POST'])
def mine_block():
    values= request.get_json()

    required = ['owner','reg_no']

    if not all(k in values for k in required):
        return 'missing values ', 400

    owner = values['owner']
    reg_no = values['reg_no']
    previous_block = blockchain.get_last_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(owner,reg_no,proof,previous_hash)

    response = {'message' : 'record will be added to the ledger'}
    return jsonify(response),200

app.run(host='0.0.0.0',port=5000,debug=True)


