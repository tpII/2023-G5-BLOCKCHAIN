/*
  SPDX-License-Identifier: Apache-2.0
*/

import {Object, Property} from 'fabric-contract-api';

/**
 * Clase que representa un activo relacionado con vinos en un contrato inteligente de Hyperledger Fabric.
 * 
 * Propiedades:
 * - docType: usado para ordenar y estructurar los assets cuando se usa couchdb como state database
 * - ID: identificación única del vino, correspondiente al RFID.
 * - Varietal: variedad de uva asociada con el vino.
 * - Owner: dueño actual del vino en la cadena de producción.
 * - Price: precio del vino.
 * - Temperature: temperatura ideal de almacenamiento del vino.
 * - Humidity: humedad relativa recomendada para el vino.
 * - Winery: bodega productora del vino.
 * - Year: año de producción del vino.
 * - Latitude: latitud de la posición geográfica del vino.
 * - Longitude: longitud de la posición geográfica del vino.
 */

@Object()
export class Asset {             
    @Property()
    public docType?: string;

    @Property()
    public ID: string;              

    @Property()
    public Varietal: string;       

    @Property()
    public Owner: string;              

    @Property()
    public Price: number;

    @Property()
    public Temperature: number;

    @Property()
    public Humidity: number;

    @Property()
    public Winery: string;

    @Property()
    public Year: string;

    @Property()
    public Latitude: number; 

    @Property()
    public Longitude: number;
}
