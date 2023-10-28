import json

import random
import string

from solcx import (
    compile_standard,
    install_solc,
)



def randomize_solidity_contract():
    contract_code = f"""
    pragma solidity ^0.8.0;

    contract SimpleStorage {{
        uint256 private storedData;

        function set(uint256 x) public {{
            storedData = {random.randint(64545, 10000000)};
        }}

        function get() public view returns (uint256) {{
            return storedData;
        }}
    }}
    """
    
    return contract_code




def compile_contract() -> None:
    install_solc('0.8.0')
    with open('src/modules/deploy/contract/contract.sol', 'r') as file:
        contract = file.read()

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"contract.sol": {"content": contract}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                    }
                }
            },
        },
        solc_version="0.8.0",
    )

    with open("compiled_code.json", "w") as file:
        json.dump(compiled_sol, file)

def compile_random_contact() -> None:
    install_solc('0.8.0')
    # with open('src/modules/deploy/contract/contract.sol', 'r') as file:
    #     contract = file.read()

    contract = randomize_solidity_contract()

    print(contract)

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"contract.sol": {"content": contract}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                    }
                }
            },
        },
        solc_version="0.8.0",
    )

    with open("compiled_code.json", "w") as file:
        json.dump(compiled_sol, file)


def get_bytecode() -> str:
    with open('compiled_code.json', 'r') as file:
        compiled_sol = json.load(file)

    bytecode = compiled_sol["contracts"]["contract.sol"]["SimpleStorage"]["evm"][
        "bytecode"
    ]["object"]
    return bytecode


def get_abi() -> str:
    with open('compiled_code.json', 'r') as file:
        compiled_sol = json.load(file)

    abi = json.loads(
        compiled_sol["contracts"]["contract.sol"]["SimpleStorage"]["metadata"]
    )["output"]["abi"]
    return abi
