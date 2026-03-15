import { NextResponse } from 'next/server';
import { getConnection } from '@/lib/snowflake';

interface OrderSummary {
  ORDER_MONTH: string;
  ORDER_COUNT: number;
  TOTAL_REVENUE: number;
  UNIQUE_CUSTOMERS: number;
}

interface NationData {
  NATION: string;
  TOTAL_REVENUE: number;
  CUSTOMER_COUNT: number;
}

interface PriorityData {
  PRIORITY: string;
  ORDER_COUNT: number;
  TOTAL_REVENUE: number;
}

interface PartData {
  PART_NAME: string;
  PART_TYPE: string;
  TOTAL_QUANTITY: number;
  TOTAL_REVENUE: number;
}

interface RecentOrder {
  O_ORDERKEY: number;
  O_ORDERDATE: string;
  CUSTOMER_NAME: string;
  O_TOTALPRICE: number;
  O_ORDERSTATUS: string;
  O_ORDERPRIORITY: string;
}

async function executeQuery<T>(conn: ReturnType<typeof import('snowflake-sdk').createConnection>, sql: string): Promise<T[]> {
  return new Promise((resolve, reject) => {
    conn.execute({
      sqlText: sql,
      complete: (err, stmt, rows) => {
        if (err) {
          console.error('Query error:', err.message);
          reject(err);
        } else {
          resolve((rows || []) as T[]);
        }
      }
    });
  });
}

export async function GET() {
  try {
    console.log('API: Getting connection...');
    const conn = await getConnection();
    console.log('API: Connection obtained, executing queries...');

    const [ordersSummary, nations, priorities, parts, recentOrders] = await Promise.all([
      executeQuery<OrderSummary>(conn, `
        SELECT DATE_TRUNC('month', O_ORDERDATE) as ORDER_MONTH, COUNT(*) as ORDER_COUNT,
               SUM(O_TOTALPRICE) as TOTAL_REVENUE, COUNT(DISTINCT O_CUSTKEY) as UNIQUE_CUSTOMERS
        FROM ORDERS WHERE O_ORDERDATE >= '1995-01-01'
        GROUP BY DATE_TRUNC('month', O_ORDERDATE) ORDER BY ORDER_MONTH
      `),
      executeQuery<NationData>(conn, `
        SELECT N.N_NAME as NATION, SUM(O.O_TOTALPRICE) as TOTAL_REVENUE, COUNT(DISTINCT C.C_CUSTKEY) as CUSTOMER_COUNT
        FROM ORDERS O JOIN CUSTOMER C ON O.O_CUSTKEY = C.C_CUSTKEY JOIN NATION N ON C.C_NATIONKEY = N.N_NATIONKEY
        GROUP BY N.N_NAME ORDER BY TOTAL_REVENUE DESC LIMIT 10
      `),
      executeQuery<PriorityData>(conn, `
        SELECT O_ORDERPRIORITY as PRIORITY, COUNT(*) as ORDER_COUNT, SUM(O_TOTALPRICE) as TOTAL_REVENUE
        FROM ORDERS GROUP BY O_ORDERPRIORITY ORDER BY ORDER_COUNT DESC
      `),
      executeQuery<PartData>(conn, `
        SELECT P.P_NAME as PART_NAME, P.P_TYPE as PART_TYPE, SUM(L.L_QUANTITY) as TOTAL_QUANTITY, SUM(L.L_EXTENDEDPRICE) as TOTAL_REVENUE
        FROM LINEITEM L JOIN PART P ON L.L_PARTKEY = P.P_PARTKEY GROUP BY P.P_NAME, P.P_TYPE ORDER BY TOTAL_REVENUE DESC LIMIT 10
      `),
      executeQuery<RecentOrder>(conn, `
        SELECT O.O_ORDERKEY, O.O_ORDERDATE, C.C_NAME as CUSTOMER_NAME, O.O_TOTALPRICE, O.O_ORDERSTATUS, O.O_ORDERPRIORITY
        FROM ORDERS O JOIN CUSTOMER C ON O.O_CUSTKEY = C.C_CUSTKEY ORDER BY O.O_ORDERDATE DESC LIMIT 100
      `),
    ]);

    console.log('API: Queries completed successfully');
    return NextResponse.json({
      ordersSummary,
      nations,
      priorities,
      parts,
      recentOrders,
    });
  } catch (error) {
    console.error('Database error:', error);
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    return NextResponse.json(
      { error: `Failed to fetch data from Snowflake: ${errorMessage}` },
      { status: 500 }
    );
  }
}
