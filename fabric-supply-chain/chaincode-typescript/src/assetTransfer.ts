/*
 * SPDX-License-Identifier: Apache-2.0
 */
// Deterministic JSON.stringify()
import {Context, Contract, Info, Returns, Transaction} from 'fabric-contract-api';
import stringify from 'json-stringify-deterministic';
import sortKeysRecursive from 'sort-keys-recursive';
import {Asset} from './asset';

// Identidad de cliente
import {ClientIdentity} from 'fabric-shim';

@Info({title: 'AssetTransfer', description: 'Smart contract for trading assets'})
export class AssetTransferContract extends Contract {

    @Transaction()
    public async InitLedger(ctx: Context): Promise<void> {

        // Mantener estos valores precargados para ejemplificar con RFID leidos 
        const assets: Asset[] = [
            {
                ID: '551fafac',
                Varietal: 'Cabernet Sauvignon',
                Owner: 'Org1MSP',
                Price: 25,
                Temperature: 14,
                Humidity: 65,
                Winery: 'Bodega A',
                Year: '2018',
                Latitude: -34.6037,
                Longitude: -58.3816,
            },
            {
                ID: '042b4e924b5f80',
                Varietal: 'Chardonnay',
                Owner: 'Org1MSP',
                Price: 30,
                Temperature: 12,
                Humidity: 60,
                Winery: 'Bodega B',
                Year: '2019',
                Latitude: -33.4489,
                Longitude: -70.6693,
            },
            {
                ID: '9277ee1a',
                Varietal: 'Malbec',
                Owner: 'Org2MSP',
                Price: 22,
                Temperature: 16,
                Humidity: 70,
                Winery: 'Bodega C',
                Year: '2020',
                Latitude: -23.5505,
                Longitude: -46.6333,
            },
            {
                ID: 'wine1',
                Varietal: 'Merlot',
                Owner: 'Org2MSP',
                Price: 28,
                Temperature: 15,
                Humidity: 68,
                Winery: 'Bodega D',
                Year: '2017',
                Latitude: -22.9068,
                Longitude: -43.1729,
            },
            {
                ID: 'wine2',
                Varietal: 'Pinot Noir',
                Owner: 'Org1MSP',
                Price: 35,
                Temperature: 13,
                Humidity: 62,
                Winery: 'Bodega E',
                Year: '2016',
                Latitude: 40.7128,
                Longitude: -74.0060,
            }
        ];

        for (const asset of assets) {
            asset.docType = 'wine';
            // example of how to write to world state deterministically
            // use convention of alphabetic order
            // we insert data in alphabetic order using 'json-stringify-deterministic' and 'sort-keys-recursive'
            // when retrieving data, in any lang, the order of data will be the same and consequently also the corresonding hash
            await ctx.stub.putState(asset.ID, Buffer.from(stringify(sortKeysRecursive(asset))));
            console.info(`Asset ${asset.ID} initialized`);
        }
    }

    // CreateAsset agrega un Asset nuevo al world state con algunos detalles
    @Transaction()
    public async CreateAsset(
        ctx: Context,
        role: string,
        id: string, 
        varietal: string,
        owner: string, 
        price: number, 
        temperature: number, 
        humidity: number, 
        winery: string, 
        year: string, 
        latitude: number, 
        longitude: number
    ): Promise<void> {

        if (role != 'admin') {
            throw new Error(`You don't have the permission WRONG ROLE`);
        }

        const exists = await this.AssetExists(ctx, id);
        if (exists) {
            throw new Error(`The asset ${id} already exists`);
        }
        
        let cid = new ClientIdentity(ctx.stub);

        if (owner != cid.getMSPID()) {
            throw new Error(`You don't have the permission WRONG MSPID`);
        }

        // Instancia de Asset con los parámetros proporcionados
        const asset: Asset = {
            ID: id,
            Varietal: varietal,
            Owner: owner,
            Price: price,
            Temperature: temperature,
            Humidity: humidity,
            Winery: winery,
            Year: year,
            Latitude: latitude,
            Longitude: longitude,
        };
        // Almacenar el Asset en el world state
        await ctx.stub.putState(id, Buffer.from(stringify(sortKeysRecursive(asset))));
    }

    // ReadAsset retorna el Asset almacenado en el world state segun el id
    @Transaction(false)
    public async ReadAsset(ctx: Context, id: string): Promise<string> {
        const assetJSON = await ctx.stub.getState(id); // get the asset from chaincode state
        if (!assetJSON || assetJSON.length === 0) {
            throw new Error(`The asset ${id} does not exist`);
        }
        return assetJSON.toString();
    }

    // UpdateAsset actualiza un Asset existente en el world state con los parametros propuestos
    @Transaction()
    public async UpdateAsset(
        ctx: Context,
        role: string,
        id: string, 
        varietal: string,
        owner: string, 
        price: number, 
        temperature: number, 
        humidity: number, 
        winery: string, 
        year: string, 
        latitude: number, 
        longitude: number
    ): Promise<void> {

        if (role != 'admin') {
            throw new Error(`You don't have the permission WRONG ROLE`);
        }

        const exists = await this.AssetExists(ctx, id);
        if (!exists) {
            throw new Error(`The asset ${id} does not exist`);
        }

        let cid = new ClientIdentity(ctx.stub);

        if (owner != cid.getMSPID()) {
            throw new Error(`You don't have the permission WRONG MSPID`);
        }

        // Sobreescribir el Asset original con el nuevo
        const updatedAsset = {
            ID: id,
            Varietal: varietal,
            Owner: owner,
            Price: price,
            Temperature: temperature,
            Humidity: humidity,
            Winery: winery,
            Year: year,
            Latitude: latitude,
            Longitude: longitude
        };
        return ctx.stub.putState(id, Buffer.from(stringify(sortKeysRecursive(updatedAsset))));
    }

    // DeleteAsset elimina determinado Asset del world state
    @Transaction()
    public async DeleteAsset(ctx: Context, role:string, id: string): Promise<void> {

        if (role != 'admin') {
            throw new Error(`You don't have the permission WRONG ROLE`);
        }

        const exists = await this.AssetExists(ctx, id);
        if (!exists) {
            throw new Error(`The asset ${id} does not exist`);
        }
        return ctx.stub.deleteState(id);
    }

    // AssetExists retorna verdadero cuando el Asset está en el world state
    @Transaction(false)
    @Returns('boolean')
    public async AssetExists(ctx: Context, id: string): Promise<boolean> {
        const assetJSON = await ctx.stub.getState(id);
        return assetJSON && assetJSON.length > 0;
    }

    // TransferAsset actualiza el dueño del Asset y retorna el viejo dueño
    @Transaction()
    public async TransferAsset(ctx: Context, role:string, id: string, newOwner: string): Promise<string> {
        
        if (role != 'admin') {
            throw new Error(`You don't have the permission WRONG ROLE`);
        }
        
        const assetString = await this.ReadAsset(ctx, id);
        const asset = JSON.parse(assetString);
        const oldOwner = asset.Owner;

        let cid = new ClientIdentity(ctx.stub);

        if (oldOwner != cid.getMSPID()) {
            throw new Error(`You don't have the permission WRONG MSPID`);
        }

        asset.Owner = newOwner;

        await ctx.stub.putState(id, Buffer.from(stringify(sortKeysRecursive(asset))));
        return oldOwner;
    }

    // GetAllAssets retorna todos los Assets del world state
    @Transaction(false)
    @Returns('string')
    public async GetAllAssets(ctx: Context): Promise<string> {
        const allResults = [];
        // range query with empty string for startKey and endKey does an open-ended query of all assets in the chaincode namespace.
        const iterator = await ctx.stub.getStateByRange('', '');
        let result = await iterator.next();
        while (!result.done) {
            const strValue = Buffer.from(result.value.value.toString()).toString('utf8');
            let record;
            try {
                record = JSON.parse(strValue);
            } catch (err) {
                console.log(err);
                record = strValue;
            }
            allResults.push(record);
            result = await iterator.next();
        }
        return JSON.stringify(allResults);
    }

    // GetAssetHistory retorna el historial de un Asset en formato de transacciones realizadas
    @Transaction(false)
    @Returns('string')
    public async GetAssetHistory(ctx: Context, id: string): Promise<string> {
        const promiseOfIterator = ctx.stub.getHistoryForKey(id);

        const results = [];
        for await (const keyMod of promiseOfIterator) {
            const resp = {
                timestamp: keyMod.timestamp,
                txid: keyMod.txId,
                data: ''
            }
            if (keyMod.isDelete) {
                resp.data = 'KEY DELETED';
            } else {
                resp.data = keyMod.value.toString();
            }
            results.push(resp);
        }
        return JSON.stringify(results);
    }

}
